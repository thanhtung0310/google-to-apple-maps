import Foundation

struct APIClient: Sendable {
  var session: URLSession = .shared

  func health() async -> Bool {
    var request = URLRequest(url: APIConfig.healthURL)
    request.timeoutInterval = 8
    do {
      let (_, response) = try await session.data(for: request)
      return (response as? HTTPURLResponse)?.statusCode == 200
    } catch {
      return false
    }
  }

  func resolve(url: String) async throws -> ResolveResponse {
    var request = URLRequest(url: APIConfig.resolveURL)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.timeoutInterval = 20
    request.httpBody = try JSONEncoder().encode(["url": url])

    let data: Data
    let response: URLResponse
    do {
      (data, response) = try await session.data(for: request)
    } catch {
      throw APIError.unreachable
    }

    guard let http = response as? HTTPURLResponse else {
      throw APIError.unreachable
    }

    let decoded = try? JSONDecoder().decode(ResolveResponse.self, from: data)
    if http.statusCode == 200, let decoded {
      return decoded
    }

    throw APIError.httpStatus(http.statusCode, decoded?.error)
  }
}
