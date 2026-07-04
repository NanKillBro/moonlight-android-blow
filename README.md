> [!NOTE]
> **English Translation version of Moonlight Assisi (Moonlight Android Blow)**: All custom Chinese UI elements, layout attributes, settings, and Java overlays have been fully localized to English in this repository. The original Chinese localizations are preserved under `app/src/main/res/values-zh-rCN`.
> *Note: The translation was performed automatically by AI (Gemini 3.5 Flash)*

# Moonlight Assisi (Moonlight Android Blow)
## This project modifies and extends the features of the official Moonlight Android client.
### If you have better ideas or feature implementations, feel free to submit a Pull Request!
### If you enjoy tech, gadgets, and gaming, follow the developer's social media accounts:
### Bilibili (https://space.bilibili.com/16893379) | YouTube (https://www.youtube.com/@AxixiTV)

This custom fork includes the following additional features:
1. **Brand New In-Game Menu UI**: A completely redesigned UI style for in-game configuration.
2. **Custom Virtual Buttons**: Full support for custom layout buttons, including import and export capabilities.
3. **Custom Resolution Settings**: Set custom streaming resolutions.
4. **Custom Bitrate Settings**: Force set custom video bitrates overriding default ranges.
5. **Advanced Mouse Emulation**: Toggle between multiple mouse modes (normal mouse, multi-touch surface mode, touchpad, disable touch screen operation, and local system cursor display).
6. **Virtual Controller Enhancements**: Optimized virtual gamepads skins and free joysticks.
7. **External Monitor Mode**: Show streaming screens on external monitors while keeping controller overlays on the phone screen.
8. **Gamepad Driver Support**: Native integration for DualShock 4 (DS4), DualSense (DS5), and Nintendo Switch Pro USB controller drivers.
9. **Streamlined Performance HUD**: Simplified overlay listing key stats: network speed, latency, decoding time, packet loss, and FPS.
10. **Custom Shortcut Key Commands**: Easily bind and send PC keyboard commands/combinations.
11. **Convenient Keyboard Access**: Easily trigger/toggle the phone's soft keyboard.
12. **Portrait Display Support**: Support for vertical streams and layouts.
13. **Side-by-Side (SBS) Mode**: Left-and-right 3D format for compatible VR/entertainment setups.
14. **Folding Screen Optimization**: Always-on-top display layout customizations.
15. **Virtual Touchpad Customization**: Set margins and speed for touchpad emulation, making camera-rotation games (e.g. World of Warcraft) playable.
16. **Force Device Vibration**: Route game vibration feedback directly to the phone's native vibration motor.
17. **Controller Debugging Tool**: Dedicated debugging screen to inspect vibration, gyroscope telemetry, and kernel info.

<img width="2560" height="1600" alt="Screenshot_20250409-180147" src="https://github.com/user-attachments/assets/25fc1ad2-c804-4597-a832-48ec1717cf9a" />

---

# Moonlight Android (Original Readme)

[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/232a8tadrrn8jv0k/branch/master?svg=true)](https://ci.appveyor.com/project/cgutman/moonlight-android/branch/master)
[![Translation Status](https://hosted.weblate.org/widgets/moonlight/-/moonlight-android/svg-badge.svg)](https://hosted.weblate.org/projects/moonlight/moonlight-android/)

[Moonlight for Android](https://moonlight-stream.org) is an open source client for NVIDIA GameStream and [Sunshine](https://github.com/LizardByte/Sunshine).

Moonlight for Android will allow you to stream your full collection of games from your Windows PC to your Android device,
whether in your own home or over the internet.

Moonlight also has a [PC client](https://github.com/moonlight-stream/moonlight-qt) and [iOS/tvOS client](https://github.com/moonlight-stream/moonlight-ios).

You can follow development on our [Discord server](https://moonlight-stream.org/discord) and help translate Moonlight into your language on [Weblate](https://hosted.weblate.org/projects/moonlight/moonlight-android/).

## Downloads
* [Google Play Store](https://play.google.com/store/apps/details?id=com.limelight)
* [Amazon App Store](https://www.amazon.com/gp/product/B00JK4MFN2)
* [F-Droid](https://f-droid.org/packages/com.limelight)
* [APK](https://github.com/moonlight-stream/moonlight-android/releases)

## Building
* Install Android Studio and the Android NDK
* Run ‘git submodule update --init --recursive’ from within moonlight-android/
* In moonlight-android/, create a file called ‘local.properties’. Add an ‘ndk.dir=’ property to the local.properties file and set it equal to your NDK directory.
* Build the APK using Android Studio or gradle

## Authors

* [Cameron Gutman](https://github.com/cgutman)  
* [Diego Waxemberg](https://github.com/dwaxemberg)  
* [Aaron Neyer](https://github.com/Aaronneyer)  
* [Andrew Hennessy](https://github.com/yetanothername)

Moonlight is the work of students at [Case Western](http://case.edu) and was
started as a project at [MHacks](http://mhacks.org).
