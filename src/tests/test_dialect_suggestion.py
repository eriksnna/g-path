from core.dialect import m_codes_in, process_codes_label, suggest_dialect


def test_m8_m9_program_on_generic_suggests_arc_dialect():
    assert suggest_dialect("M08\nG1 X10 F100\nM09", "generico") == "arco-m8-m9"


def test_no_suggestion_when_current_dialect_matches():
    assert suggest_dialect("M3 S1000\nG1 X10 F100\nM5", "generico") is None


def test_coolant_m8_does_not_trigger_when_spindle_codes_exist():
    assert suggest_dialect("M3\nM8\nG1 X10 F100\nM9\nM5", "generico") is None


def test_m_codes_in_comments_are_ignored():
    assert m_codes_in("G1 X1 (M8 liga)\n; M9\nM30") == {30}


def test_no_suggestion_without_process_codes():
    assert suggest_dialect("G1 X10 F100\nM30", "generico") is None


def test_process_codes_label():
    assert process_codes_label("arco-m8-m9") == "M8/M9"