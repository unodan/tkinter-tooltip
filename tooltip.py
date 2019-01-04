from tkinter import Label as tkLabel
from tkinter import Toplevel, TclError


class Tooltip:
    def __init__(self, widget, text, delay=750, duration=1500):
        self.widget = widget
        self._tooltip = None

        self._hide_id = None
        self._render_id = None
        self._tooltip_text = text
        self._tooltip_delay = delay
        self._tooltip_duration = duration

        self._enter_bind = self.widget.bind("<Enter>", self.show)
        self._leave_bind = self.widget.bind("<Leave>", self.hide)
        self._button_bind = self.widget.bind("<Button>", self.hide)

    def __del__(self):
        try:
            self.widget.unbind("<Enter>", self._enter_bind)
            self.widget.unbind("<Leave>", self._leave_bind)
            self.widget.unbind("<Button>", self._button_bind)
        except TclError:
            pass

    def show(self, _):
        def render():
            if not self._tooltip:
                self._tooltip = tw = Toplevel(self.widget)
                tw.wm_overrideredirect(True)

                x, y = 20, self.widget.winfo_height() + 1
                root_x = self.widget.winfo_rootx() + x
                root_y = self.widget.winfo_rooty() + y
                self._tooltip.wm_geometry("+%d+%d" % (root_x, root_y))

                label = tkLabel(
                    self._tooltip,
                    text=self._tooltip_text,
                    justify='left',
                    background="#ffffe0",
                    relief='solid',
                    borderwidth=1
                )
                label.pack()
                self._tooltip.update_idletasks()  # Needed on MacOS -- see #34275.
                self._tooltip.lift()
                self._hide_id = self.widget.after(self._tooltip_duration, self.hide)

        if self._tooltip_delay:
            if self._render_id:
                self.widget.after_cancel(self._render_id)
            self._render_id = self.widget.after(self._tooltip_delay, render)
        else:
            render()

    def hide(self, _=None):
        try:
            if self._hide_id:
                self.widget.after_cancel(self._hide_id)
            if self._render_id:
                self.widget.after_cancel(self._render_id)
        except TclError:
            pass

        tooltip = self._tooltip
        if self._tooltip:
            try:
                tooltip.destroy()
            except TclError:
                pass
            self._tooltip = None

    @property
    def delay(self):
        return self._tooltip_delay

    @delay.setter
    def delay(self, value):
        self._tooltip_delay = value

    @property
    def duration(self):
        return self._tooltip_duration

    @duration.setter
    def duration(self, value):
        self._tooltip_duration = value

    @property
    def tooltip_text(self):
        return self._tooltip_text

    @tooltip_text.setter
    def tooltip_text(self, value):
        self._tooltip_text = value