from Components.Sources.Source import Source

class Strings(Source):
	def __init__(self):
		Source.__init__(self)

	"""
	This returns all string the webinterface requires, currently translated into the language that's configured in e2
	With a small hack it should be possible to actually return the strings in the browser's/requester's language
	"""
	def getList(self):
		return [
			["television" , _("TeleVision")],
			["tv", _("TV")],
			["radio" , _("Radio")],
			["movies" , _("Movies")],
			["timer" , _("Timer")],
			["timers" , _("Timers")],
			["boxcontrol" , _("BoxControl")],
			["extras" , _("Extras")],
			["webtv" , _("WebTV")],
			["volume" , _("Volume")],
			["epgsearch" , _("EPG-Search")],
			["epgsearch_hint" , _("Search EPG")],
			["clear_serach" , _("Clear search")],
			["bouquets" , _("Bouquets")],
			["no_bouquets", _("No Bouquets to Display")],
			["select_bouquet", _("Please select any bouquet")],
			["providers", _("Providers")],
			["satellites", _("Satellites")],
			["all" , _("All")],
			["tagfilter" , _("Tag Filter")],
			["all_timers" , _("All Timers")],
			["create_timer" , _("Create Timer")],
			["cleanup" , _("Cleanup")],
			["note_timerlist_cleanup", _("Cleans up the list of timers by removing e.g. finished timers")],
			["no_timer", _("No Timer Available!")],
			["edit_timer", _("Edit Timer")],
			["enable", _("Enable")],
			["activate", _("Activate")],
			["deactivate", _("Deactivate")],
			["disable", _("Disable")],
			["delete", _("Delete")],
			["delete_timer" , _("Delete Timer")],
			["legend", _("Legend")],
			["waiting", _("Waiting")],
			["error", _("Error")],
			["running", _("Running")],
			["finished", _("Finished")],
			["action" , _("Action")],
			["record" , _("Record")],
			["zap" , _("Zap")],
			["note_recurring_events", _("Note: For recurring events dates are not mandatory.")],
			["note_onetime_events", _("Note: For one-time events the days don't have to be specified.")],
			["begins" , _("Begins")],
			["ends" , _("Ends")],
			["days" , _("Days")],
			["channel" , _("Channel")],
			["name" , _("Name")],
			["description" , _("Description")],
			["location" , _("Location")],
			["tags" , _("Tags")],
			["afterevent" , _("After event")],
			["do_nothing" , _("Do Nothing")],
			["of", _("of")],
			["standby" , _("Idle Mode")],
			["shutdown" , _("Shutdown")],
			["auto" , _("Auto")],
			["save" , _("Save")],
			["powercontrol" , _("Power Control")],
			["send_message" , _("Send Message")],
			["webremote" , _("WebRemote")],
			["screenshot_all" , _("Screenshot (All)")],
			["screenshot_video" , _("Screenshot (Video)")],
			["screenshot_osd" , _("Screenshot (OSD)")],
			["screenshot_display", _("Screenshot (Display)")],
			["toggle_standby" , _("Toggle Idle Mode")],
			["deepstanby" , _("Standby")],
			["reboot" , _("Reboot")],
			["restart_enigma2" , _("Restart GUI")],
			["message" , _("Message")],
			["timeout" , _("Timeout")],
			["type" , _("Type")],
			["info" , _("Info")],
			["warning" , _("Warning")],
			["error" , _("Error")],
			["send" , _("Send")],
			["send_message" , _("Send Message")],
			["mediaplayer" , _("Mediaplayer")],
			["deviceinfo" , _("Device Info")],
			["settings" , _("Settings")],
			["tools" , _("Tools")],
			["about" , _("About")],
			["show_hide_extended_desc" , _("Click to show/hide extended description")],
			["show_epg_for" , _("Show EPG for %s")],
			["stream_channel" , _("Stream %s")],
			["do_stream", _("Stream")],
			["instant_record" , _("Instant Record")],
			["record_current_event" , _("Record current event")],
			["start_record_infinite" , _("Start infinite recording")],
			["open_signal_panel" , _("Open Signal Panel")],
			["zap_to_channel" , _("Zap to %s")],
			["open_multi_epg_for" , _("Open Multi-EPG for %s")],
			["load_bouquet", _("Load Bouquet")],
			["playlist_for", _("Playlist for %s")],
			["imdb_lookup", _("Lookup on IMDb.com")],
			["add_timer", _("Add Timer")],
			["add_zap_timer", _("Add Zap Timer")],
			["edit_timer", _("Edit Timer")],
			["no_service", _("No Service to show")],
			["select_submenu", _("please select a submenu on the left...")],
			["filter_services", _("Filter Services")],
			["authors", _("Authors")],
			["many_contributors", _("and many contributors")],
			["javscript_libraries", _("JavaScript Libraries")],
			["license", _("License")],
			["device_and_versions", _("Device & Versions")],
			["device_name", _("Device Name")],
			["engima2_version", _("Dreambox OS Version")],
			["image_version", _("Image Version")],
			["frontprocessor_version", _("Frontprocessor Version")],
			["webinterface_version", _("Webinterface Version")],
			["tuners", _("Tuners")],
			["harrdisk", _("Harddisk")],
			["capacity", _("Capacity")],
			["free_space", _("Free Space")],
			["network_interface", _("Network Interface")],
			["mac_address", _("Mac Address")],
			["dhcp_enabled", _("DHCP enabled")],
			["ip_address", _("IP Address")],
			["netmask", _("Netmask")],
			["gateway", _("Gateway")],
			["videosize", _("Video Size")],
			["widescreen", _("Widescreen")],
			["apid", _("Audio PID")],
			["vpid", _("Video PID")],
			["pcrpid", _("PCR PID")],
			["pmtpid", _("PMT PID")],
			["txtpid", _("Text PID")],
			["tsid", _("TSID")],
			["onid", _("ONID")],
			["sid", _("SID")],
			["nothing_running", _("Nothing running...")],
			["technical_information", _("Technical Information")],
			["nothing_found", _("Nothing found...")],
			["no_movies", _("No movies to show...")],
			["download", _("Download")],
			["volume_down", _("Volume Down")],
			["down", _("Down")],
			["mute", _("Mute")],
			["unmute", _("Unmute")],
			["volume_up", _("Volume Up")],
			["up", _("Up")],
			["get_screenshot", _("Get a Screenshot")],
			["grab_video_and_osd", _("Grab Video & OSD")],
			["send_long_keypress", _("Send \\\"long\\\" keypress")],
			["refresh_screenshot", _("Refresh Screenshot")],
			["settings_cookies_required", _("WARNING: Cookies are required to store the settings!")],
			["enable_debug", _("Enable Debug")],
			["update_interval_current_service", _("Update interval for current service (min. 10 sec)")],
			["update_interval_current_bouquet_epg", _("Update-Interval for EPG of the current bouquets (min. 60 sec)")],
			["seconds_short", _("sec")],
			["previous", _("Previous")],
			["play", _("Play")],
			["play_item", _("Play %s")],
			["add_item_to_playlist", _("Add %s to playlist")],
			["remove_item_from_playlist", _("Remove %s from playlist")],
			["download_item", _("Downlad %s")],
			["delete_item", _("Delete %s")],
			["change_to_item", _("Change to %s")],
			["next", _("Next")],
			["stop", _("Stop")],
			["filebrowser", _("Filebrowser")],
			["playlist", _("Playlist")],
			["save_playlist", _("Save Playlist")],
			["close_mediaplayer", _("Close MediaPlayer")],
			["no_items", _("No items to show...")],
			["remaining_minutes", _("%s of %s min")],
			["enable_encoder", _("Enable encoder")],
			["rtsp_port", _("RTSP Port")],
			["rtsp_path", _("RTSP Path")],
			["video_bitrate", _("Video Bitrate")],
			["audio_bitrate", _("Audio Bitrate")],
			["encoder_settings_hint", _("You have to set your encoder into TV-Services Mode for things to work as expected!")],
		]

	list = property(getList)
	lut = { "id": 0, "value": 1 }
