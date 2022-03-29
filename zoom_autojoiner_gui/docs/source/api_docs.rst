==================
API Documentation
==================

Create an extension
-------------------

To start creating extensions, one must register extensions. To do so, import the ExtensionAPI class and pass the extension name and version:

.. code-block:: python

    from zoom_autojoiner_gui.extensions import ExtensionAPI

    ext_api = ExtensionAPI(__name__, "extension_name", ver="0.1.0")

Here, ``extension_name`` represents the extension's name.

Register menu items
--------------------

The ``tkinter.Menu`` class needs to be imported. Proceed as you would normally, except for two things:

#. Do not attach a parent to ``tkinter.Menu`` (even though ``ExtensionAPI.menu_bar`` is the menu bar element, don't use it as extensions are loaded before the main application is loaded, even before tkinter is imported!)
#. Instead of adding a cascade to the main menu, use the ``register_menu`` method of ``ExtensionAPI``, the reason being the same as above.

An example is given below:

.. code-block:: python

    mnu = tk.Menu(tearoff="off") # no parent
    mnu.add_command(label="test", command=test)
    mnu.add_command(label="test2", command=test2)
    # ... you can have further entries
    ext_api.register_menu(mnu) # instead of ExtensionAPI.ext_menu.add_cascade(...)

Event Listeners
----------------

Event listeners are functions that are executed when a particular event occurs. For example, when the application is loaded, the ``application_loaded`` event is fired.

List of Event Listeners
~~~~~~~~~~~~~~~~~~~~~~~~

Currently, two event listeners exist, with several yet to be implemented:

.. list-table::
   :widths: 25 5 70
   :header-rows: 1

   * - Event Listener
     - Implemented
     - Description
   * - ``test``
     - ⛔
     - For unit testing. Not to be used by extensions.
   * - ``application_loaded``
     - ✅
     - When the Tkinter frame has loaded, just before executing Mainloop. All objects are available for use.
   * - ``add_meeting``
     - ❌
     - When the New Meeting menu item is clicked, this event is fired.
   * - ``edit_meeting``
     - ❌
     - When the Edit Meeting button is clicked, this event is fired.
   * - ``join_meeting``
     - ❌
     - When the Join Meeting button is clicked, this event is fired.
   * - ``no_autojoiner_callback_error``
     - ✅
     - When no autojoiner callback is found for a given provider, the exception is forwarded to this event listener. An argument, e is passed with the exception.

Key:

* ⛔ Reserved
* ✅ Available
* ❌ Not yet implemented

Adding an event listener function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add an event listener function, one must use the ``add_event_listener`` method of ``ExtensionAPI``. Two arguments to be passed are the event listener and the callback.

Example:

.. code-block:: python

    def cb():
        print("Hello World")

    ext_api.add_event_listener("application_loaded", cb)

Verify that 'Hello World' is printed by using the Debugging Tools extension.

Proceed with error handlers in a similar way. This is the callback function for ``no_autojoiner_callback_error`` in Extensionfather, which shows the error dialog:

.. code-block:: python

    def error_no_callback(error):
        messagebox.showerror("Error", "There is no Autojoiner registered for "
                                    "this meeting provider. Please install and"
                                    " enable the extension which has the"
                                    " required functionality.")

    # ...

    ext_api.add_event_listener("no_autojoiner_callback_error", error_no_callback)

Autojoiners
-----------

Autojoiners are registered in a similar way to event listeners.

All autojoiners need a provider. This is a short and unique string (preferably all caps) used to identify the meeting provider. For example, you can use the following:

.. list-table::
   :widths: 25 5 70
   :header-rows: 1

   * - Provider
     - Implemented
     - Description
   * - ZM
     - ⛔
     - Zoom
   * - GMEET
     - ✅
     - Google Meet
   * - SKYPE
     - ❌
     - Skype
   * - MST
     - ❌
     - Microsoft Teams
   * - WBX
     - ❌
     - Webex
   * - JITSI
     - ❌
     - Jitsi Meet (`meet.jit.si <https://meet.jit.si>`_)

Key:

* ⛔ Reserved (implemented in core)
* ✅ Implemented in an extension
* ❌ Not yet implemented (just suggestions for names)

All callbacks are passed two arguments - the meeting ID and password. Have a look at the below function:

.. code-block:: python

    def callback(mtg_id, mtg_pw):
        ...
        # do whatever you want
    

    ext_api.register_autojoiner_callback("provider", callback)
    # provider from above table

.. note::

    There is no GUI interface to change the meeting provider - hence all meetings created with ``Meetings -> New Meeting`` will be only Zoom Meetings. A temporary solution (till an interface is implemented natively) would be to create a separate Toplevel window to do the same. See the ``gmeet_autojoiner`` extension for more info.