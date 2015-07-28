# freedomfy
Open music software for personal library management and streaming.

## Purpose

I really like the basic idea behind services like Spotify and Google Play Music All Access, where your library is stored in the cloud and you can access it from anywhere, and easily add new music at any time. This project is inspired by those, but has a different set of goals:

* **Openness.** You shouldn't be stuck with whatever awful decisions or designs some faceless corporation thrusts upon you. This project aims to be a free software alternative that anyone can tweak to whatever niche functionality they want.
* **Pro user support.** Popular music services aim to please the lowest common denominator, and have only features that anyone can easily use. That's great for them, but I want more powerful tools. For this project, advanced functionality is higher priority than usability and intuitiveness.
* **Personal use.** Whereas popular music streaming services live on one massive cloud shared by all users, this project is designed so that each instance is only to be used by one user or a handful of users. This will simplify many aspects of development and allow more time to be spent on other features.

## Wishlist

These are the features and design decisions I would like for this application. Italicized features are considered low priority, and should not be worked on before v1.0 is complete.

* Server software. Should maintain database of all songs and playlists, and be able to serve and receive music files from a variety of sources.
  * probably gonna use Node.js?
* Web app, for accessing music collection via browser
  * Perhaps use [BinaryJS](http://binaryjs.com/) for streaming?
* Android app, for accessing music collection via Android device (can use [this sample](https://github.com/googlesamples/android-UniversalMusicPlayer) as basis)
* Easy integration with big platforms for importing/exporting/etc:
  * Bandcamp
  * Google Play Music All Access
  * SoundCloud
  * _Last.fm_
  * _Spotify_
  * _YouTube_
* _Pull music metadata from Gracenote_
* _Multiple users_

## License

This project is licensed under the MIT license; see [this page](http://oxguy3.mit-license.org) for details.
