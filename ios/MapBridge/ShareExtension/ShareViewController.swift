import UIKit
import SwiftUI
import UniformTypeIdentifiers

final class ShareViewController: UIViewController {
  override func viewDidLoad() {
    super.viewDidLoad()
    view.backgroundColor = .systemBackground
    Task { await bootstrap() }
  }

  @MainActor
  private func bootstrap() async {
    let url = await extractSharedURL()
    let root = ShareConvertView(
      initialURL: url,
      open: { [weak self] url in self?.extensionContext?.open(url) },
      onDone: { [weak self] in self?.extensionContext?.completeRequest(returningItems: nil) }
    )
    let host = UIHostingController(rootView: root)
    addChild(host)
    host.view.frame = view.bounds
    host.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
    view.addSubview(host.view)
    host.didMove(toParent: self)
  }

  private func extractSharedURL() async -> String {
    guard let items = extensionContext?.inputItems as? [NSExtensionItem] else { return "" }
    for item in items {
      for provider in item.attachments ?? [] {
        if provider.hasItemConformingToTypeIdentifier(UTType.url.identifier),
           let value = try? await provider.loadItem(forTypeIdentifier: UTType.url.identifier),
           let url = value as? URL {
          return url.absoluteString
        }
        if provider.hasItemConformingToTypeIdentifier(UTType.plainText.identifier),
           let value = try? await provider.loadItem(forTypeIdentifier: UTType.plainText.identifier),
           let text = value as? String {
          if let found = firstURL(in: text) { return found }
          return text.trimmingCharacters(in: .whitespacesAndNewlines)
        }
      }
    }
    return ""
  }

  private func firstURL(in text: String) -> String? {
    let detector = try? NSDataDetector(types: NSTextCheckingResult.CheckingType.link.rawValue)
    let range = NSRange(text.startIndex..., in: text)
    return detector?.firstMatch(in: text, options: [], range: range)?.url?.absoluteString
  }
}

struct ShareConvertView: View {
  let initialURL: String
  let open: (URL) -> Void
  let onDone: () -> Void

  @State private var pin: LastPin?
  @State private var errorMessage: String?
  @State private var didStart = false

  var body: some View {
    NavigationStack {
      VStack(alignment: .leading, spacing: 16) {
        if let pin {
          Text(pin.displayTitle)
            .font(.headline)
          Text(pin.coordinateLabel)
            .font(.footnote)
            .foregroundStyle(.secondary)
          Button("Open in \(pin.targetPlatform ?? "Maps")") {
            if let url = MapsOpener.webURL(for: pin) {
              open(url)
            }
          }
          .buttonStyle(.borderedProminent)
        } else if let errorMessage {
          Text(errorMessage)
            .foregroundStyle(.red)
        } else {
          ProgressView("Converting…")
        }
        Spacer()
      }
      .padding()
      .navigationTitle("Map Bridge")
      .navigationBarTitleDisplayMode(.inline)
      .toolbar {
        ToolbarItem(placement: .cancellationAction) {
          Button("Done", action: onDone)
        }
      }
      .task {
        guard !didStart else { return }
        didStart = true
        await convert()
      }
    }
  }

  private func convert() async {
    let input = initialURL.trimmingCharacters(in: .whitespacesAndNewlines)
    guard !input.isEmpty else {
      errorMessage = "No map link found in this share."
      return
    }
    do {
      let response = try await APIClient().resolve(url: input)
      let resolved = LastPin(from: response)
      pin = resolved
      LastPinStore.shared.save(resolved)
    } catch {
      errorMessage = error.localizedDescription
    }
  }
}
