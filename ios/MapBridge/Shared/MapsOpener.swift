import Foundation

#if os(watchOS)
import MapKit
#endif

/// URL building only. UIApplication is unavailable in app extensions, so each
/// target performs the actual open: the app uses UIApplication, the Share
/// Extension uses its extensionContext, and the Watch uses MapKit.
enum MapsOpener {
  /// Native scheme first, https fallback second.
  static func candidateURLs(for pin: LastPin) -> [URL] {
    pin.targetPlatform == "Google Maps" ? googleURLs(for: pin) : appleURLs(for: pin)
  }

  static func appleURLs(for pin: LastPin) -> [URL] {
    let query = encodedQuery(for: pin)
    let native = URL(string: "maps://?ll=\(pin.lat),\(pin.lng)&q=\(query)")
    let web = URL(string: pin.appleUrl ?? "https://maps.apple.com/?ll=\(pin.lat),\(pin.lng)&q=\(query)")
    return [native, web].compactMap { $0 }
  }

  static func googleURLs(for pin: LastPin) -> [URL] {
    let coordQuery = "\(pin.lat),\(pin.lng)"
    let native = URL(string: "comgooglemaps://?center=\(pin.lat),\(pin.lng)&q=\(coordQuery)")
    let web = URL(string: pin.googleUrl ?? "https://www.google.com/maps/search/?api=1&query=\(coordQuery)")
    return [native, web].compactMap { $0 }
  }

  /// https universal link, safe where `canOpenURL` cannot be checked.
  static func webURL(for pin: LastPin) -> URL? {
    if let target = pin.targetUrl, let url = URL(string: target) { return url }
    return candidateURLs(for: pin).last
  }

  #if os(watchOS)
  static func openAppleMapsOnWatch(_ pin: LastPin, startNavigation: Bool) {
    let coordinate = CLLocationCoordinate2D(latitude: pin.lat, longitude: pin.lng)
    let item = MKMapItem(placemark: MKPlacemark(coordinate: coordinate))
    item.name = pin.displayTitle
    var options: [String: Any] = [:]
    if startNavigation {
      options[MKLaunchOptionsDirectionsModeKey] = MKLaunchOptionsDirectionsModeDriving
    }
    item.openInMaps(launchOptions: options)
  }
  #endif

  private static func encodedQuery(for pin: LastPin) -> String {
    let raw = pin.name?.isEmpty == false ? pin.name! : pin.coordinateLabel
    return raw.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? raw
  }
}
