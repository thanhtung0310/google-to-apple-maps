import SwiftUI
import UIKit

struct ContentView: View {
  @State private var urlText = ""
  @State private var isResolving = false
  @State private var errorMessage: String?
  @State private var result: LastPin?
  private let client = APIClient()

  var body: some View {
    NavigationStack {
      ScrollView {
        VStack(alignment: .leading, spacing: 16) {
          Text("Google Maps ⇆ Apple Maps")
            .font(.caption.weight(.semibold))
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(.white)
            .clipShape(Capsule())

          Text("Universal Map Bridge")
            .font(.title.bold())

          Text("Paste a Google Maps or Apple Maps link, or share one via the share sheet.")
            .font(.subheadline)
            .foregroundStyle(.secondary)

          TextField("Paste Apple or Google Maps link...", text: $urlText, axis: .vertical)
            .textFieldStyle(.roundedBorder)
            .textInputAutocapitalization(.never)
            .autocorrectionDisabled()
            .lineLimit(3...6)

          HStack {
            Button("Paste") {
              if let value = UIPasteboard.general.string, !value.isEmpty {
                urlText = value.trimmingCharacters(in: .whitespacesAndNewlines)
              }
            }
            .buttonStyle(.bordered)

            Button(isResolving ? "Resolving Location..." : "Convert Link") {
              Task { await convert() }
            }
            .buttonStyle(.borderedProminent)
            .tint(.black)
            .disabled(isResolving || urlText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
          }

          if let errorMessage {
            Text(errorMessage)
              .font(.footnote.weight(.semibold))
              .foregroundStyle(.red)
          }

          if let result {
            VStack(alignment: .leading, spacing: 12) {
              Text(result.displayTitle)
                .font(.headline)
              Text(result.coordinateLabel)
                .font(.footnote)
                .foregroundStyle(.secondary)
              if let detected = result.detectedPlatform {
                Text("From \(detected)")
                  .font(.footnote)
                  .foregroundStyle(.secondary)
              }
              Button("Open in \(result.targetPlatform ?? "Maps")") {
                AppMapsOpener.openTarget(for: result)
              }
              .buttonStyle(.borderedProminent)
              .tint(result.targetPlatform == "Google Maps" ? Color(red: 0.26, green: 0.52, blue: 0.96) : Color(red: 0.19, green: 0.82, blue: 0.35))
            }
            .padding()
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(.white)
            .clipShape(RoundedRectangle(cornerRadius: 16))
          }
        }
        .padding(24)
      }
      .background(
        LinearGradient(colors: [Color(red: 0.63, green: 0.77, blue: 0.99), Color(red: 0.76, green: 0.91, blue: 0.98)], startPoint: .topLeading, endPoint: .bottomTrailing)
          .ignoresSafeArea()
      )
      .navigationBarTitleDisplayMode(.inline)
    }
  }

  @MainActor
  private func convert() async {
    errorMessage = nil
    result = nil
    let input = urlText.trimmingCharacters(in: .whitespacesAndNewlines)
    guard !input.isEmpty else {
      errorMessage = "Please enter a valid link."
      return
    }
    isResolving = true
    defer { isResolving = false }
    do {
      let response = try await client.resolve(url: input)
      let pin = LastPin(from: response)
      result = pin
      WatchSessionManager.shared.pushLastPin(pin)
    } catch {
      errorMessage = error.localizedDescription
    }
  }
}

enum AppMapsOpener {
  static func openTarget(for pin: LastPin) {
    let application = UIApplication.shared
    let candidates = MapsOpener.candidateURLs(for: pin)
    for url in candidates where application.canOpenURL(url) {
      application.open(url)
      return
    }
    if let fallback = candidates.last {
      application.open(fallback)
    }
  }
}

#Preview {
  ContentView()
}
