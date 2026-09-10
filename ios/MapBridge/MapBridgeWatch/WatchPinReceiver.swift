import Foundation
import WatchConnectivity

@MainActor
final class WatchPinReceiver: NSObject, ObservableObject, WCSessionDelegate {
  @Published var pin: LastPin?

  override init() {
    super.init()
    pin = LastPinStore.shared.load()
    guard WCSession.isSupported() else { return }
    WCSession.default.delegate = self
    WCSession.default.activate()
  }

  private func apply(_ context: [String: Any]) {
    guard let received = LastPin.fromApplicationContext(context) else { return }
    LastPinStore.shared.save(received)
    pin = received
  }

  nonisolated func session(
    _ session: WCSession,
    activationDidCompleteWith activationState: WCSessionActivationState,
    error: Error?
  ) {
    Task { @MainActor in
      if !session.receivedApplicationContext.isEmpty {
        self.apply(session.receivedApplicationContext)
      }
    }
  }

  nonisolated func session(_ session: WCSession, didReceiveApplicationContext applicationContext: [String: Any]) {
    Task { @MainActor in
      self.apply(applicationContext)
    }
  }

  nonisolated func session(_ session: WCSession, didReceiveUserInfo userInfo: [String: Any] = [:]) {
    Task { @MainActor in
      self.apply(userInfo)
    }
  }
}
