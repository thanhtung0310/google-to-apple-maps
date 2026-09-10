import SwiftUI

@main
struct MapBridgeWatchApp: App {
  @StateObject private var receiver = WatchPinReceiver()

  var body: some Scene {
    WindowGroup {
      WatchContentView()
        .environmentObject(receiver)
    }
  }
}
