#!/usr/bin/env python3
"""Generate MapBridge.xcodeproj/project.pbxproj"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJ = ROOT / "MapBridge.xcodeproj"
PROJ.mkdir(exist_ok=True)

def uid(n: int) -> str:
    return f"A{n:023X}"

files = {
    "AppConstants.swift": "Shared/AppConstants.swift",
    "APIConfig.swift": "Shared/APIConfig.swift",
    "ResolveResponse.swift": "Shared/ResolveResponse.swift",
    "APIError.swift": "Shared/APIError.swift",
    "APIClient.swift": "Shared/APIClient.swift",
    "LastPin.swift": "Shared/LastPin.swift",
    "LastPinStore.swift": "Shared/LastPinStore.swift",
    "MapsOpener.swift": "Shared/MapsOpener.swift",
    "MapBridgeApp.swift": "MapBridge/MapBridgeApp.swift",
    "ContentView.swift": "MapBridge/ContentView.swift",
    "WatchSessionManager.swift": "MapBridge/WatchSessionManager.swift",
    "iOSInfo.plist": "MapBridge/Info.plist",
    "iOSEntitlements": "MapBridge/MapBridge.entitlements",
    "iOSAssets": "MapBridge/Assets.xcassets",
    "ShareViewController.swift": "ShareExtension/ShareViewController.swift",
    "ShareInfo.plist": "ShareExtension/Info.plist",
    "ShareEntitlements": "ShareExtension/ShareExtension.entitlements",
    "MapBridgeWatchApp.swift": "MapBridgeWatch/MapBridgeWatchApp.swift",
    "WatchContentView.swift": "MapBridgeWatch/WatchContentView.swift",
    "WatchPinReceiver.swift": "MapBridgeWatch/WatchPinReceiver.swift",
    "WatchInfo.plist": "MapBridgeWatch/Info.plist",
    "WatchEntitlements": "MapBridgeWatch/MapBridgeWatch.entitlements",
    "WatchAssets": "MapBridgeWatch/Assets.xcassets",
    "Debug.xcconfig": "Config/Debug.xcconfig",
    "Release.xcconfig": "Config/Release.xcconfig",
}

ids = {name: uid(i + 1) for i, name in enumerate(files)}
build = {}
n = 100
for name in files:
    build[name + "_ios"] = uid(n); n += 1
    build[name + "_watch"] = uid(n); n += 1
    build[name + "_share"] = uid(n); n += 1

IOS = uid(200)
WATCH = uid(201)
SHARE = uid(202)
PROJECT = uid(203)
IOS_CONFIG_LIST = uid(210)
WATCH_CONFIG_LIST = uid(211)
SHARE_CONFIG_LIST = uid(212)
PROJECT_CONFIG_LIST = uid(213)
IOS_DEBUG = uid(220)
IOS_RELEASE = uid(221)
WATCH_DEBUG = uid(222)
WATCH_RELEASE = uid(223)
SHARE_DEBUG = uid(224)
SHARE_RELEASE = uid(225)
PROJECT_DEBUG = uid(226)
PROJECT_RELEASE = uid(227)
IOS_SOURCES = uid(230)
WATCH_SOURCES = uid(231)
SHARE_SOURCES = uid(232)
IOS_RESOURCES = uid(233)
WATCH_RESOURCES = uid(234)
SHARE_RESOURCES = uid(235)
IOS_FRAMEWORKS = uid(236)
WATCH_FRAMEWORKS = uid(237)
SHARE_FRAMEWORKS = uid(238)
EMBED_WATCH = uid(240)
EMBED_EXT = uid(241)
WATCH_PROXY = uid(242)
SHARE_PROXY = uid(243)
WATCH_DEP = uid(244)
SHARE_DEP = uid(245)
IOS_PRODUCT = uid(250)
WATCH_PRODUCT = uid(251)
SHARE_PRODUCT = uid(252)
WKCONN_IOS = uid(260)
WKCONN_WATCH = uid(261)
MAPKIT_WATCH = uid(262)
WKCONN_IOS_REF = uid(263)
WKCONN_WATCH_REF = uid(264)
MAPKIT_REF = uid(265)
GROUP_ROOT = uid(270)
GROUP_SHARED = uid(271)
GROUP_IOS = uid(272)
GROUP_WATCH = uid(273)
GROUP_SHARE = uid(274)
GROUP_CONFIG = uid(275)
GROUP_PRODUCTS = uid(276)
GROUP_FW = uid(277)

shared_sources = [
    "AppConstants.swift", "APIConfig.swift", "ResolveResponse.swift", "APIError.swift",
    "APIClient.swift", "LastPin.swift", "LastPinStore.swift", "MapsOpener.swift",
]
ios_only = ["MapBridgeApp.swift", "ContentView.swift", "WatchSessionManager.swift"]
watch_only = ["MapBridgeWatchApp.swift", "WatchContentView.swift", "WatchPinReceiver.swift"]
share_only = ["ShareViewController.swift"]

def fileref(name, last_known="sourcecode.swift"):
    path = files[name]
    return f'\t\t{ids[name]} /* {path} */ = {{isa = PBXFileReference; lastKnownFileType = {last_known}; path = {Path(path).name}; sourceTree = "<group>"; }};\n'

def buildfile(bid, ref, comment):
    return f"\t\t{bid} /* {comment} in Sources */ = {{isa = PBXBuildFile; fileRef = {ref} /* {comment} */; }};\n"

pbx_build = ""
for s in shared_sources + ios_only:
    pbx_build += buildfile(build[s + "_ios"], ids[s], Path(files[s]).name)
for s in shared_sources + watch_only:
    pbx_build += buildfile(build[s + "_watch"], ids[s], Path(files[s]).name)
for s in shared_sources + share_only:
    pbx_build += buildfile(build[s + "_share"], ids[s], Path(files[s]).name)

pbx_build += f"\t\t{build['iOSAssets_ios']} /* Assets.xcassets in Resources */ = {{isa = PBXBuildFile; fileRef = {ids['iOSAssets']} /* Assets.xcassets */; }};\n"
pbx_build += f"\t\t{build['WatchAssets_watch']} /* Assets.xcassets in Resources */ = {{isa = PBXBuildFile; fileRef = {ids['WatchAssets']} /* Assets.xcassets */; }};\n"
pbx_build += f"\t\t{WKCONN_IOS} /* WatchConnectivity.framework in Frameworks */ = {{isa = PBXBuildFile; fileRef = {WKCONN_IOS_REF} /* WatchConnectivity.framework */; }};\n"
pbx_build += f"\t\t{WKCONN_WATCH} /* WatchConnectivity.framework in Frameworks */ = {{isa = PBXBuildFile; fileRef = {WKCONN_WATCH_REF} /* WatchConnectivity.framework */; }};\n"
pbx_build += f"\t\t{MAPKIT_WATCH} /* MapKit.framework in Frameworks */ = {{isa = PBXBuildFile; fileRef = {MAPKIT_REF} /* MapKit.framework */; }};\n"
pbx_build += f"\t\t{uid(280)} /* MapBridgeWatch.app in Embed Watch Content */ = {{isa = PBXBuildFile; fileRef = {WATCH_PRODUCT} /* MapBridgeWatch.app */; settings = {{ATTRIBUTES = (RemoveHeadersOnCopy, ); }}; }};\n"
pbx_build += f"\t\t{uid(281)} /* MapBridgeShare.appex in Embed Foundation Extensions */ = {{isa = PBXBuildFile; fileRef = {SHARE_PRODUCT} /* MapBridgeShare.appex */; settings = {{ATTRIBUTES = (RemoveHeadersOnCopy, ); }}; }};\n"

refs = ""
for name, path in files.items():
    p = Path(path)
    if name.endswith("Info.plist") or name in ("iOSInfo.plist", "ShareInfo.plist", "WatchInfo.plist"):
        refs += fileref(name, "text.plist.xml")
    elif "Entitlements" in name:
        refs += fileref(name, "text.plist.entitlements")
    elif path.endswith(".xcassets"):
        refs += f'\t\t{ids[name]} /* {p.name} */ = {{isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = {p.name}; sourceTree = "<group>"; }};\n'
    elif path.endswith(".xcconfig"):
        refs += fileref(name, "text.xcconfig")
    else:
        refs += fileref(name)

refs += f'\t\t{IOS_PRODUCT} /* MapBridge.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = MapBridge.app; sourceTree = BUILT_PRODUCTS_DIR; }};\n'
refs += f'\t\t{WATCH_PRODUCT} /* MapBridgeWatch.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = MapBridgeWatch.app; sourceTree = BUILT_PRODUCTS_DIR; }};\n'
refs += f'\t\t{SHARE_PRODUCT} /* MapBridgeShare.appex */ = {{isa = PBXFileReference; explicitFileType = "wrapper.app-extension"; includeInIndex = 0; path = MapBridgeShare.appex; sourceTree = BUILT_PRODUCTS_DIR; }};\n'
refs += f'\t\t{WKCONN_IOS_REF} /* WatchConnectivity.framework */ = {{isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = WatchConnectivity.framework; path = System/Library/Frameworks/WatchConnectivity.framework; sourceTree = SDKROOT; }};\n'
refs += f'\t\t{WKCONN_WATCH_REF} /* WatchConnectivity.framework */ = {{isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = WatchConnectivity.framework; path = System/Library/Frameworks/WatchConnectivity.framework; sourceTree = SDKROOT; }};\n'
refs += f'\t\t{MAPKIT_REF} /* MapKit.framework */ = {{isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = MapKit.framework; path = System/Library/Frameworks/MapKit.framework; sourceTree = SDKROOT; }};\n'
refs += f'\t\t{ids["Debug.xcconfig"]} /* Debug.xcconfig */;\n'

# wait Debug already in files loop

def children(names):
    lines = []
    for n in names:
        lines.append(f"\t\t\t\t{ids[n]} /* {Path(files[n]).name} */,")
    return "\n".join(lines)

groups = f'''
		{GROUP_ROOT} = {{
			isa = PBXGroup;
			children = (
				{GROUP_SHARED} /* Shared */,
				{GROUP_IOS} /* MapBridge */,
				{GROUP_WATCH} /* MapBridgeWatch */,
				{GROUP_SHARE} /* ShareExtension */,
				{GROUP_CONFIG} /* Config */,
				{GROUP_FW} /* Frameworks */,
				{GROUP_PRODUCTS} /* Products */,
			);
			sourceTree = "<group>";
		}};
		{GROUP_SHARED} /* Shared */ = {{
			isa = PBXGroup;
			children = (
{children(shared_sources)}
			);
			path = Shared;
			sourceTree = "<group>";
		}};
		{GROUP_IOS} /* MapBridge */ = {{
			isa = PBXGroup;
			children = (
{children(ios_only + ["iOSInfo.plist", "iOSEntitlements", "iOSAssets"])}
			);
			path = MapBridge;
			sourceTree = "<group>";
		}};
		{GROUP_WATCH} /* MapBridgeWatch */ = {{
			isa = PBXGroup;
			children = (
{children(watch_only + ["WatchInfo.plist", "WatchEntitlements", "WatchAssets"])}
			);
			path = MapBridgeWatch;
			sourceTree = "<group>";
		}};
		{GROUP_SHARE} /* ShareExtension */ = {{
			isa = PBXGroup;
			children = (
{children(share_only + ["ShareInfo.plist", "ShareEntitlements"])}
			);
			path = ShareExtension;
			sourceTree = "<group>";
		}};
		{GROUP_CONFIG} /* Config */ = {{
			isa = PBXGroup;
			children = (
				{ids["Debug.xcconfig"]} /* Debug.xcconfig */,
				{ids["Release.xcconfig"]} /* Release.xcconfig */,
			);
			path = Config;
			sourceTree = "<group>";
		}};
		{GROUP_FW} /* Frameworks */ = {{
			isa = PBXGroup;
			children = (
				{WKCONN_IOS_REF} /* WatchConnectivity.framework */,
				{MAPKIT_REF} /* MapKit.framework */,
			);
			name = Frameworks;
			sourceTree = "<group>";
		}};
		{GROUP_PRODUCTS} /* Products */ = {{
			isa = PBXGroup;
			children = (
				{IOS_PRODUCT} /* MapBridge.app */,
				{WATCH_PRODUCT} /* MapBridgeWatch.app */,
				{SHARE_PRODUCT} /* MapBridgeShare.appex */,
			);
			name = Products;
			sourceTree = "<group>";
		}};
'''

def sources_phase(phase_id, names, suffix):
    kids = ",\n".join(f"\t\t\t\t{build[n + suffix]} /* {Path(files[n]).name} in Sources */" for n in names)
    return f'''
		{phase_id} = {{
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
{kids}
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
'''

sources = sources_phase(IOS_SOURCES, shared_sources + ios_only, "_ios")
sources += sources_phase(WATCH_SOURCES, shared_sources + watch_only, "_watch")
sources += sources_phase(SHARE_SOURCES, shared_sources + share_only, "_share")

resources = f'''
		{IOS_RESOURCES} = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{build["iOSAssets_ios"]} /* Assets.xcassets in Resources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{WATCH_RESOURCES} = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{build["WatchAssets_watch"]} /* Assets.xcassets in Resources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{SHARE_RESOURCES} = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{IOS_FRAMEWORKS} = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{WKCONN_IOS} /* WatchConnectivity.framework in Frameworks */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{WATCH_FRAMEWORKS} = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{WKCONN_WATCH} /* WatchConnectivity.framework in Frameworks */,
				{MAPKIT_WATCH} /* MapKit.framework in Frameworks */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{SHARE_FRAMEWORKS} = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{EMBED_WATCH} = {{
			isa = PBXCopyFilesBuildPhase;
			buildActionMask = 2147483647;
			dstPath = "$(CONTENTS_FOLDER_PATH)/Watch";
			dstSubfolderSpec = 16;
			files = (
				{uid(280)} /* MapBridgeWatch.app in Embed Watch Content */,
			);
			name = "Embed Watch Content";
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{EMBED_EXT} = {{
			isa = PBXCopyFilesBuildPhase;
			buildActionMask = 2147483647;
			dstPath = "";
			dstSubfolderSpec = 13;
			files = (
				{uid(281)} /* MapBridgeShare.appex in Embed Foundation Extensions */,
			);
			name = "Embed Foundation Extensions";
			runOnlyForDeploymentPostprocessing = 0;
		}};
'''

# Duplicate Debug.xcconfig file ref - I accidentally appended extra. Remove that from refs generation.

# Fix refs - I had a bug adding Debug twice. The files loop already includes Debug.xcconfig.

# Remove the erroneous extra line from refs in this script - I had:
# refs += f'\t\t{ids["Debug.xcconfig"]} /* Debug.xcconfig */;\n'
# I need to not include that incomplete line. Looking at my code... I have a comment "wait Debug already" after adding incomplete line. Let me not add it.

targets = f'''
		{IOS} /* MapBridge */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {IOS_CONFIG_LIST} /* Build configuration list for PBXNativeTarget "MapBridge" */;
			buildPhases = (
				{IOS_SOURCES} /* Sources */,
				{IOS_FRAMEWORKS} /* Frameworks */,
				{IOS_RESOURCES} /* Resources */,
				{EMBED_WATCH} /* Embed Watch Content */,
				{EMBED_EXT} /* Embed Foundation Extensions */,
			);
			buildRules = (
			);
			dependencies = (
				{WATCH_DEP} /* PBXTargetDependency */,
				{SHARE_DEP} /* PBXTargetDependency */,
			);
			name = MapBridge;
			productName = MapBridge;
			productReference = {IOS_PRODUCT} /* MapBridge.app */;
			productType = "com.apple.product-type.application";
		}};
		{WATCH} /* MapBridgeWatch */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {WATCH_CONFIG_LIST} /* Build configuration list for PBXNativeTarget "MapBridgeWatch" */;
			buildPhases = (
				{WATCH_SOURCES} /* Sources */,
				{WATCH_FRAMEWORKS} /* Frameworks */,
				{WATCH_RESOURCES} /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
			);
			name = MapBridgeWatch;
			productName = MapBridgeWatch;
			productReference = {WATCH_PRODUCT} /* MapBridgeWatch.app */;
			productType = "com.apple.product-type.application";
		}};
		{SHARE} /* MapBridgeShare */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {SHARE_CONFIG_LIST} /* Build configuration list for PBXNativeTarget "MapBridgeShare" */;
			buildPhases = (
				{SHARE_SOURCES} /* Sources */,
				{SHARE_FRAMEWORKS} /* Frameworks */,
				{SHARE_RESOURCES} /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
			);
			name = MapBridgeShare;
			productName = MapBridgeShare;
			productReference = {SHARE_PRODUCT} /* MapBridgeShare.appex */;
			productType = "com.apple.product-type.app-extension";
		}};
'''

proxies = f'''
		{WATCH_PROXY} /* PBXContainerItemProxy */ = {{
			isa = PBXContainerItemProxy;
			containerPortal = {PROJECT} /* Project object */;
			proxyType = 1;
			remoteGlobalIDString = {WATCH};
			remoteInfo = MapBridgeWatch;
		}};
		{SHARE_PROXY} /* PBXContainerItemProxy */ = {{
			isa = PBXContainerItemProxy;
			containerPortal = {PROJECT} /* Project object */;
			proxyType = 1;
			remoteGlobalIDString = {SHARE};
			remoteInfo = MapBridgeShare;
		}};
		{WATCH_DEP} /* PBXTargetDependency */ = {{
			isa = PBXTargetDependency;
			target = {WATCH} /* MapBridgeWatch */;
			targetProxy = {WATCH_PROXY} /* PBXContainerItemProxy */;
		}};
		{SHARE_DEP} /* PBXTargetDependency */ = {{
			isa = PBXTargetDependency;
			target = {SHARE} /* MapBridgeShare */;
			targetProxy = {SHARE_PROXY} /* PBXContainerItemProxy */;
		}};
'''

common_debug = """
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_TESTABILITY = YES;
				GCC_DYNAMIC_NO_PIC = NO;
				GCC_OPTIMIZATION_LEVEL = 0;
				MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
				ONLY_ACTIVE_ARCH = YES;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = "DEBUG $(inherited)";
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
				SWIFT_VERSION = 5.0;
"""

common_release = """
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				MTL_ENABLE_DEBUG_INFO = NO;
				SWIFT_COMPILATION_MODE = wholemodule;
				SWIFT_VERSION = 5.0;
"""

ios_settings = f"""
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				CODE_SIGN_ENTITLEMENTS = MapBridge/MapBridge.entitlements;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = MapBridge/Info.plist;
				INFOPLIST_KEY_CFBundleDisplayName = "Map Bridge";
				INFOPLIST_KEY_LSApplicationCategoryType = "public.app-category.navigation";
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations = UIInterfaceOrientationPortrait;
				IPHONEOS_DEPLOYMENT_TARGET = 17.0;
				LD_RUNPATH_SEARCH_PATHS = "$(inherited) @executable_path/Frameworks";
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.mapbridge.app;
				PRODUCT_NAME = MapBridge;
				SDKROOT = iphoneos;
				SUPPORTED_PLATFORMS = "iphoneos iphonesimulator";
				SUPPORTS_MACCATALYST = NO;
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = 1;
"""

watch_settings = f"""
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				CODE_SIGN_ENTITLEMENTS = MapBridgeWatch/MapBridgeWatch.entitlements;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = MapBridgeWatch/Info.plist;
				INFOPLIST_KEY_CFBundleDisplayName = "Map Bridge";
				INFOPLIST_KEY_WKApplication = YES;
				INFOPLIST_KEY_WKCompanionAppBundleIdentifier = com.mapbridge.app;
				LD_RUNPATH_SEARCH_PATHS = "$(inherited) @executable_path/Frameworks";
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.mapbridge.app.watchkitapp;
				PRODUCT_NAME = MapBridgeWatch;
				SDKROOT = watchos;
				SKIP_INSTALL = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = 4;
				WATCHOS_DEPLOYMENT_TARGET = 10.0;
"""

share_settings = f"""
				CODE_SIGN_ENTITLEMENTS = ShareExtension/ShareExtension.entitlements;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				GENERATE_INFOPLIST_FILE = NO;
				INFOPLIST_FILE = ShareExtension/Info.plist;
				IPHONEOS_DEPLOYMENT_TARGET = 17.0;
				LD_RUNPATH_SEARCH_PATHS = "$(inherited) @executable_path/Frameworks @executable_path/../../Frameworks";
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.mapbridge.app.share;
				PRODUCT_MODULE_NAME = MapBridgeShare;
				PRODUCT_NAME = MapBridgeShare;
				SDKROOT = iphoneos;
				SKIP_INSTALL = YES;
				SUPPORTED_PLATFORMS = "iphoneos iphonesimulator";
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = 1;
"""

configs = f'''
		{PROJECT_DEBUG} /* Debug */ = {{
			isa = XCBuildConfiguration;
			baseConfigurationReference = {ids["Debug.xcconfig"]} /* Debug.xcconfig */;
			buildSettings = {{{common_debug}
			}};
			name = Debug;
		}};
		{PROJECT_RELEASE} /* Release */ = {{
			isa = XCBuildConfiguration;
			baseConfigurationReference = {ids["Release.xcconfig"]} /* Release.xcconfig */;
			buildSettings = {{{common_release}
			}};
			name = Release;
		}};
		{IOS_DEBUG} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{{ios_settings}
			}};
			name = Debug;
		}};
		{IOS_RELEASE} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{{ios_settings}
			}};
			name = Release;
		}};
		{WATCH_DEBUG} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{{watch_settings}
			}};
			name = Debug;
		}};
		{WATCH_RELEASE} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{{watch_settings}
			}};
			name = Release;
		}};
		{SHARE_DEBUG} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{{share_settings}
			}};
			name = Debug;
		}};
		{SHARE_RELEASE} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{{share_settings}
			}};
			name = Release;
		}};
		{PROJECT_CONFIG_LIST} /* Build configuration list for PBXProject "MapBridge" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{PROJECT_DEBUG} /* Debug */,
				{PROJECT_RELEASE} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
		{IOS_CONFIG_LIST} /* Build configuration list for PBXNativeTarget "MapBridge" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{IOS_DEBUG} /* Debug */,
				{IOS_RELEASE} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
		{WATCH_CONFIG_LIST} /* Build configuration list for PBXNativeTarget "MapBridgeWatch" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{WATCH_DEBUG} /* Debug */,
				{WATCH_RELEASE} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
		{SHARE_CONFIG_LIST} /* Build configuration list for PBXNativeTarget "MapBridgeShare" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{SHARE_DEBUG} /* Debug */,
				{SHARE_RELEASE} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
'''

# Fix refs: remove accidental incomplete Debug line if present
refs = "\n".join(line for line in refs.splitlines() if not line.strip().endswith("/* Debug.xcconfig */;")) + "\n"

project = f'''// !$*UTF8*$!
{{
	archiveVersion = 1;
	classes = {{
	}};
	objectVersion = 56;
	objects = {{
/* Begin PBXBuildFile section */
{pbx_build}/* End PBXBuildFile section */

/* Begin PBXContainerItemProxy section */
{proxies}/* End PBXContainerItemProxy section */

/* Begin PBXFileReference section */
{refs}/* End PBXFileReference section */

/* Begin PBXFrameworksBuildPhase section */
{resources}/* End PBXCopyFilesBuildPhase section */

/* Begin PBXGroup section */
{groups}/* End PBXGroup section */

/* Begin PBXNativeTarget section */
{targets}/* End PBXNativeTarget section */

		{PROJECT} /* Project object */ = {{
			isa = PBXProject;
			attributes = {{
				BuildIndependentTargetsInParallel = 1;
				LastSwiftUpdateCheck = 1540;
				LastUpgradeCheck = 1540;
				TargetAttributes = {{
					{IOS} = {{ CreatedOnToolsVersion = 15.4; }};
					{WATCH} = {{ CreatedOnToolsVersion = 15.4; }};
					{SHARE} = {{ CreatedOnToolsVersion = 15.4; }};
				}};
			}};
			buildConfigurationList = {PROJECT_CONFIG_LIST} /* Build configuration list for PBXProject "MapBridge" */;
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = {GROUP_ROOT};
			productRefGroup = {GROUP_PRODUCTS} /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				{IOS} /* MapBridge */,
				{WATCH} /* MapBridgeWatch */,
				{SHARE} /* MapBridgeShare */,
			);
		}};

/* Begin PBXSourcesBuildPhase section */
{sources}/* End PBXSourcesBuildPhase section */

/* Begin XCBuildConfiguration section */
{configs}/* End XCConfigurationList section */
	}};
	rootObject = {PROJECT} /* Project object */;
}}
'''

(PROJ / "project.pbxproj").write_text(project)
print("wrote", PROJ / "project.pbxproj")
