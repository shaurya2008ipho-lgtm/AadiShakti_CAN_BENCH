from pathlib import Path
import cantools

ROOT = Path(__file__).resolve().parents[1]
DB = cantools.database.load_file(str(ROOT / "dbc" / "aadi_shakti_demo.dbc"))


def test_engine_dynamics_roundtrip():
    msg = DB.get_message_by_name("ENGINE_DYNAMICS")
    payload = msg.encode({"RPM": 4600, "CHT": 685, "EGT": 842, "Vibration": 2.1})
    decoded = msg.decode(payload)
    assert abs(decoded["RPM"] - 4600) < 1e-6
    assert abs(decoded["CHT"] - 685) < 1e-6
    assert abs(decoded["EGT"] - 842) < 1e-6
    assert abs(decoded["Vibration"] - 2.1) < 1e-6
