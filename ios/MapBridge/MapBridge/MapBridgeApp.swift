import SwiftUI

@main
struct MapBridgeApp: App {
  init() {
    WatchSessionManager.shared.activate()
  }

  var body: some Scene {
    WindowGroup {
      ContentView()
        .onAppear {
          WatchSessionManager.shared.syncStoredPinToWatch()
        }
    }
  }
}
