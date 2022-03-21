import unittest

import zoom_autojoiner_gui.views


class AutojoinerClassTestCase(unittest.TestCase):
    def test_autojoiner_adding(self):
        def cb(id, pw): pass
        zoom_autojoiner_gui.views.Autojoiner.register_autojoiner("ZUMBA", cb)
        self.assertTrue("ZUMBA" in zoom_autojoiner_gui.views.Autojoiner.autojoiner_handlers)
        self.assertEqual(zoom_autojoiner_gui.views.Autojoiner.autojoiner_handlers["ZUMBA"],
                         cb)




if __name__=="__main__":
    unittest.main(verbosity=2)
