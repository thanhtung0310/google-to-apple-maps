import Foundation

final class LastPinStore: @unchecked Sendable {
  static let shared = LastPinStore()

  private let defaults: UserDefaults?

  init(defaults: UserDefaults? = nil) {
    if let defaults {
      self.defaults = defaults
      return
    }
    #if os(watchOS)
    self.defaults = .standard
    #else
    self.defaults = UserDefaults(suiteName: AppConstants.appGroupID) ?? .standard
    #endif
  }

  func load() -> LastPin? {
    guard let data = defaults?.data(forKey: AppConstants.lastPinDefaultsKey) else { return nil }
    return try? JSONDecoder().decode(LastPin.self, from: data)
  }

  func save(_ pin: LastPin) {
    guard let data = try? JSONEncoder().encode(pin) else { return }
    defaults?.set(data, forKey: AppConstants.lastPinDefaultsKey)
    CFNotificationCenterPostNotification(
      CFNotificationCenterGetDarwinNotifyCenter(),
      CFNotificationName(AppConstants.lastPinDarwinName),
      nil,
      nil,
      true
    )
  }
}
