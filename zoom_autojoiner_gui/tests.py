import unittest

import zoom_autojoiner_gui.controllers
import zoom_autojoiner_gui.extensions

class AutojoinerClassTestCase(unittest.TestCase):
    def test_autojoiner_adding(self):
        def cb(id, pw): pass
        zoom_autojoiner_gui.views.Autojoiner.register_autojoiner("ZUMBA", cb)
        self.assertTrue("ZUMBA" in zoom_autojoiner_gui.views.Autojoiner.autojoiner_handlers)
        self.assertEqual(zoom_autojoiner_gui.views.Autojoiner.autojoiner_handlers["ZUMBA"],
                         cb)
class ExtensionClassTestCase(unittest.TestCase):
    def setUp(self):
        self.ext = zoom_autojoiner_gui.extensions.ExtensionAPI(__name__, 
                                                               'tests')

    def tearDown(self):
        self.ext.reg_eventlisteners["test"].clear()
        del self.ext
        
    def test_nonexistent_eventlistener_adding(self):
        def cb(): pass
        try:
            # Nobody names an event after a person,
            # hence it is better than putting something like
            # 'fail' or 'testfail' or 'abc' etc.
            self.ext.add_event_listener("john", cb)
        except Exception as e:
            self.assertIsInstance(e, 
                zoom_autojoiner_gui.extensions.NoSuchEventError)
        else:
            self.assertTrue(False) # no error - is not intended
            
    def test_existent_eventlistener_adding(self):
        def cb(): pass
        self.ext.add_event_listener("test", cb)
        self.assertIn(cb, self.ext.reg_eventlisteners["test"])
    
    def test_existent_eventlistener_calling(self):
        a = 18
        b = 21
        c = "Pi"
        def cb():
            nonlocal a
            a = 50
        def cb2():
            nonlocal b
            b = 314
        def cb3():
            nonlocal c
            c = "Zeta"
        self.ext.add_event_listener("test", cb)
        self.ext.add_event_listener("test", cb2)
        self.ext.add_event_listener("test", cb3)
        self.ext.event_occured("test")
        self.assertEqual(a, 50)
        self.assertEqual(b, 314)
        self.assertEqual(c, "Zeta")
        
    def test_existent_eventlistener_calling_only1(self):
        a = 18
        b = 21
        c = "Pi"
        def cb1():
            nonlocal a
            a = 50
        def cb2():
            nonlocal b
            b = 314
        def cb3():
            nonlocal c
            c = "Zeta"
        self.ext.add_event_listener("test", cb1)
        self.ext.add_event_listener("test", cb2)
        self.ext.add_event_listener("test", cb3)
        self.ext.event_occured("test", onlydefault=True)
        self.assertEqual(a, 50)
        self.assertEqual(b, 21)
        self.assertEqual(c, "Pi")
        



if __name__=="__main__":
    unittest.main(verbosity=2)
