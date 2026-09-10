import SwiftUI

struct WatchContentView: View {
  @EnvironmentObject private var receiver: WatchPinReceiver

  var body: some View {
    NavigationStack {
      if let pin = receiver.pin {
        ScrollView {
          VStack(alignment: .leading, spacing: 8) {
            Text(pin.displayTitle)
              .font(.headline)
            Text(pin.coordinateLabel)
              .font(.caption2)
              .foregroundStyle(.secondary)
            if let detected = pin.detectedPlatform {
              Text("From \(detected)")
                .font(.caption2)
                .foregroundStyle(.secondary)
            }
            Text(pin.resolvedAt.formatted(date: .omitted, time: .shortened))
              .font(.caption2)
              .foregroundStyle(.secondary)
            Button("Open in Maps") {
              MapsOpener.openAppleMapsOnWatch(pin, startNavigation: false)
            }
            Button("Start Navigation") {
              MapsOpener.openAppleMapsOnWatch(pin, startNavigation: true)
            }
          }
        }
        .navigationTitle("Map Bridge")
      } else {
        ContentUnavailableView(
          "No pin yet",
          systemImage: "map",
          description: Text("Convert or share a Maps link on iPhone to send it here.")
        )
      }
    }
  }
}
