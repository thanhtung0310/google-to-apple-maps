import Foundation

/// Debug builds talk to the local Express server. Release builds must use HTTPS.
/// Set `MAPBRIDGE_API_BASE_URL` in Config/Release.xcconfig (no localhost in Release).
enum APIConfig {
  static var baseURL: URL {
    if let raw = Bundle.main.object(forInfoDictionaryKey: "MAPBRIDGE_API_BASE_URL") as? String {
      let trimmed = raw.trimmingCharacters(in: .whitespacesAndNewlines)
      if let url = URL(string: trimmed), !trimmed.isEmpty, !trimmed.contains("YOUR_MAPBRIDGE_HOST") {
        return url
      }
    }
    #if DEBUG
    return URL(string: "http://127.0.0.1:3000")!
    #else
    // Replace YOUR_MAPBRIDGE_HOST in Config/Release.xcconfig. Never use localhost in Release (ATS).
    return URL(string: "https://mapbridge.invalid")!
    #endif
  }

  static var resolveURL: URL {
    baseURL.appending(path: "api/resolve")
  }

  static var healthURL: URL {
    baseURL.appending(path: "api/health")
  }
}
