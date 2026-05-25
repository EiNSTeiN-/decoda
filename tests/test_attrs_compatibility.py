from decoda.exceptions import UnknownReferenceError
from decoda.main import BitLength, PGN, SPN, ScalarValue, UnknownPGN
from decoda.transport import Decoda


class _NoKnownPgns:
    def get_by_id(self, id):
        raise UnknownReferenceError(f"PGN not found for id: {id}")


class _Spec:
    PGNs = _NoKnownPgns()


def test_attrs_models_used_by_the_generator_integration_accept_positional_args():
    value_decoder = ScalarValue("rpm", 0, 8031.875, 0, 0.125, BitLength(16))
    spn = SPN(190, "Engine Speed", "Engine speed", value_decoder)
    pgn = PGN(
        61444,
        "EEC1",
        "Electronic Engine Controller 1",
        None,
        BitLength(64),
        [],
    )

    assert spn.id == 190
    assert spn.value_decoder is value_decoder
    assert pgn.id == 61444
    assert pgn.ordering_records == []


def test_unknown_pgn_keeps_payload_for_custom_dm1_decoding():
    payload = bytes([0x55, 0x55, 0x80, 0x06, 0x07, 0x03])
    messages = []

    Decoda(_Spec(), messages.append).handle_message(6, 0, -1, 65226, payload)

    assert len(messages) == 1
    assert isinstance(messages[0].pgn, UnknownPGN)
    assert messages[0].pgn.id == 65226
    assert messages[0].pgn.payload == payload
