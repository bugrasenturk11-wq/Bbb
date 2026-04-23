import unittest

from jarvis import RuntimeState, _handle


class JarvisTests(unittest.TestCase):
    def test_max_mode_toggle(self):
        state = RuntimeState()
        self.assertIn("KAPALI", _handle("maxmod durum", state))
        self.assertIn("etkinleştirildi", _handle("maxmod ac", state))
        self.assertTrue(state.max_mode)
        self.assertIn("AÇIK", _handle("maxmod durum", state))

    def test_note_flow(self):
        state = RuntimeState()
        self.assertIn("Not alındı (1)", _handle("not deneme", state))
        self.assertIn("1. deneme", _handle("notlar", state))

    def test_phone_command_dispatch(self):
        state = RuntimeState()

        def fake_exec(cmd):
            if cmd == ["adb", "devices"]:
                return 0, "List of devices attached\nABC123\tdevice", ""
            return 1, "", "unexpected"

        out = _handle("telefon durum", state, executor=fake_exec)
        self.assertIn("ABC123", out)


if __name__ == "__main__":
    unittest.main()
