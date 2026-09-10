import Foundation

struct ResolveResponse: Codable, Sendable {
  let success: Bool?
  let lat: Double
  let lng: Double
  let name: String?
  let detectedPlatform: String?
  let targetPlatform: String?
  let targetUrl: String?
  let appleUrl: String?
  let googleUrl: String?
  let error: String?
}
