import Foundation
import WatchConnectivity

final class WatchSessionManager: NSObject, ObservableObject, WCSessionDelegate {
  static let shared = WatchSessionManager()

  override init() {
    super.init()
    activate()
    startDarwinObserver()
  }

  func activate() {
    guard WCSession.isSupported() else { return }
    WCSession.default.delegate = self
    WCSession.default.activate()
  }

  func pushLastPin(_ pin: LastPin) {
    LastPinStore.shared.save(pin)
    sendToWatch(pin)
  }

  func syncStoredPinToWatch() {
    if let pin = LastPinStore.shared.load() {
      sendToWatch(pin)
    }
  }

  private func sendToWatch(_ pin: LastPin) {
    guard WCSession.isSupported() else { return }
    let session = WCSession.default
    guard session.activationState == .activated else { return }
    guard let context = try? pin.applicationContext() else { return }
    try? session.updateApplicationContext(context)
    session.transferUserInfo(context)
  }

  private func startDarwinObserver() {
    let center = CFNotificationCenterGetDarwinNotifyCenter()
    let observer = Unmanaged.passUnretained(self).toOpaque()
    CFNotificationCenterAddObserver(
      center,
      observer,
      { _, observer, _, _, _ in
        guard let observer else { return }
        let manager = Unmanaged<WatchSessionManager>.fromOpaque(observer).takeUnretainedValue()
        DispatchQueue.main.async {
          manager.syncStoredPinToWatch()
        }
      },
      AppConstants.lastPinDarwinName,
      nil,
      .deliverImmediately
    )
  }

  func session(
    _ session: WCSession,
    activationDidCompleteWith activationState: WCSessionActivationState,
    error: Error?
  ) {
    DispatchQueue.main.async {
      self.syncStoredPinToWatch()
    }
  }

  func sessionDidBecomeInactive(_ session: WCSession) {}

  func sessionDidDeactivate(_ session: WCSession) {
    session.activate()
  }
}
