import Foundation

struct LastPin: Codable, Equatable, Sendable {
  var lat: Double
  var lng: Double
  var name: String?
  var detectedPlatform: String?
  var targetPlatform: String?
  var appleUrl: String?
  var googleUrl: String?
  var targetUrl: String?
  var resolvedAt: Date

  init(from response: ResolveResponse, resolvedAt: Date = Date()) {
    self.lat = response.lat
    self.lng = response.lng
    self.name = response.name
    self.detectedPlatform = response.detectedPlatform
    self.targetPlatform = response.targetPlatform
    self.appleUrl = response.appleUrl
    self.googleUrl = response.googleUrl
    self.targetUrl = response.targetUrl
    self.resolvedAt = resolvedAt
  }

  var coordinateLabel: String {
    String(format: "%.6f, %.6f", lat, lng)
  }

  var displayTitle: String {
    if let name, !name.isEmpty { return name }
    return coordinateLabel
  }

  func applicationContext() throws -> [String: Any] {
    let encoder = JSONEncoder()
    encoder.dateEncodingStrategy = .iso8601
    let data = try encoder.encode(self)
    guard let object = try JSONSerialization.jsonObject(with: data) as? [String: Any] else {
      return [:]
    }
    return object
  }

  static func fromApplicationContext(_ context: [String: Any]) -> LastPin? {
    guard JSONSerialization.isValidJSONObject(context),
          let data = try? JSONSerialization.data(withJSONObject: context) else {
      return nil
    }
    let decoder = JSONDecoder()
    decoder.dateDecodingStrategy = .iso8601
    return try? decoder.decode(LastPin.self, from: data)
  }
}
