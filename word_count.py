from gi.repository import GObject, Gedit

class WordCountPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "WordCountPlugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        try:
            # Get statusbar and context
            self.statusbar = self.window.get_statusbar()
            self.context_id = self.statusbar.get_context_id("word-count")

            # Initial word count update
            self.update_word_count()

            # Connect signals
            self.handler_id_tab_added = self.window.connect("tab-added", self.on_tab_added)
            self.handler_id_active_tab_changed = self.window.connect("active-tab-changed", self.on_active_tab_changed)

            print("Word Count Plugin activated")
        except Exception as e:
            print(f"Error during activation: {e}")

    def do_deactivate(self):
        try:
            # Disconnect signals
            self.window.disconnect(self.handler_id_tab_added)
            self.window.disconnect(self.handler_id_active_tab_changed)

            # Clean up statusbar
            self.statusbar.remove_all(self.context_id)

            print("Word Count Plugin deactivated")
        except Exception as e:
            print(f"Error during deactivation: {e}")

    def on_tab_added(self, window, tab):
        try:
            # Connect to the buffer change signal
            view = tab.get_view()
            view.get_buffer().connect("changed", self.on_text_changed)

            # Initial word count update for new tab
            self.update_word_count()
        except Exception as e:
            print(f"Error in on_tab_added: {e}")

    def on_active_tab_changed(self, window, tab):
        try:
            # Update word count when switching tabs
            self.update_word_count()
        except Exception as e:
            print(f"Error in on_active_tab_changed: {e}")

    def on_text_changed(self, buffer):
        try:
            # Update word count when text changes
            self.update_word_count()
        except Exception as e:
            print(f"Error in on_text_changed: {e}")

    def update_word_count(self):
        try:
            # Get the active tab and its document
            tab = self.window.get_active_tab()
            if tab is None:
                return

            doc = tab.get_document()
            text = doc.get_text(doc.get_start_iter(), doc.get_end_iter(), True)
            word_count = len(text.split())

            # Update statusbar with word count
            self.statusbar.push(self.context_id, f"Words: {word_count}")
        except Exception as e:
            print(f"Error in update_word_count: {e}")
