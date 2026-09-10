import Foundation

enum APIError: LocalizedError {
  case invalidURL
  case httpStatus(Int, String?)
  case decoding
  case unreachable

  var errorDescription: String? {
    switch self {
    case .invalidURL:
      return "Invalid API URL."
    case .httpStatus(let code, let message):
      if let message, !message.isEmpty { return message }
      if code == 422 { return "Could not extract coordinates from the provided link." }
      return "Server error (\(code))."
    case .decoding:
      return "Unexpected response from the server."
    case .unreachable:
      return "Server unreachable. Start the API (`npm start`) or set MAPBRIDGE_API_BASE_URL."
    }
  }
}
