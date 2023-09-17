ALPHABET = "BCDFGHJKLMNPQRSTVWXYZ0123456789-"


def pw_to_num(pw: str):
    assert isinstance(pw, str)
    num = 0
    for c in reversed(pw):
        num = num << 5 | ALPHABET.index(c)
    return num


def num_to_pw(num: int):
    assert isinstance(num, int)
    pw = ""
    for i in range(5):
        pw += ALPHABET[(num >> (5 * i)) & 0x1F]
    return pw


def check_difficulty(passwd_as_num):
    uVar1 = passwd_as_num & 0x8208
    if uVar1 == 0x8208 or uVar1 == 0x200 or uVar1 == 8:
        return True
    return False


def check_levels(passwd_as_num):
    if get_bit(passwd_as_num, 23) != 0 and passwd_as_num & 0x400110 != 0x400000:
        return False
    if (get_bit(passwd_as_num, 22) != 0) and (get_bit(passwd_as_num, 6) != 0):
        return False
    if (get_bit(passwd_as_num, 8) == 0) and (get_bit(passwd_as_num, 13) == 0):
        return False
    if (get_bit(passwd_as_num, 4) == 0) and (get_bit(passwd_as_num, 14) == 0):
        return False
    return True


def check_secondary_bits(passwd_as_num):
    if (
        get_bit(passwd_as_num, 1)
        ^ get_bit(passwd_as_num, 11)
        ^ get_bit(passwd_as_num, 20)
        ^ get_bit(passwd_as_num, 4)
        ^ get_bit(passwd_as_num, 3)
    ) != get_bit(passwd_as_num, 0):
        return False
    if (
        get_bit(passwd_as_num, 2)
        ^ get_bit(passwd_as_num, 7)
        ^ get_bit(passwd_as_num, 20)
        ^ get_bit(passwd_as_num, 8)
        ^ get_bit(passwd_as_num, 15)
    ) != get_bit(passwd_as_num, 5):
        return False
    if (
        get_bit(passwd_as_num, 10)
        ^ get_bit(passwd_as_num, 16)
        ^ get_bit(passwd_as_num, 20)
        ^ get_bit(passwd_as_num, 4)
        ^ get_bit(passwd_as_num, 15)
    ) != get_bit(passwd_as_num, 18):
        return False
    if (
        get_bit(passwd_as_num, 0)
        ^ get_bit(passwd_as_num, 12)
        ^ get_bit(passwd_as_num, 17)
        ^ get_bit(passwd_as_num, 23)
        ^ get_bit(passwd_as_num, 9)
    ) != get_bit(passwd_as_num, 21):
        return False
    if (
        get_bit(passwd_as_num, 5)
        ^ get_bit(passwd_as_num, 18)
        ^ get_bit(passwd_as_num, 19)
        ^ get_bit(passwd_as_num, 6)
        ^ get_bit(passwd_as_num, 3)
    ) != get_bit(passwd_as_num, 24):
        return False

    return True


def check(pw: str):
    assert isinstance(pw, str)
    passwd_as_num = pw_to_num(pw)
    if not check_secondary_bits(passwd_as_num):
        return False
    if not check_difficulty(passwd_as_num):
        return False
    if not check_levels(passwd_as_num):
        return False
    return True


def decode(pw: str):
    assert isinstance(pw, str)
    assert check(pw)
    passwd_as_num = pw_to_num(pw)
    return {
        "belt": get_bit(passwd_as_num, 1),
        "left_wrist": get_bit(passwd_as_num, 2),
        "right_wrist": get_bit(passwd_as_num, 7) ^ 1,
        "thermal_suit": get_bit(passwd_as_num, 10) ^ 1,
        "armor_suit": get_bit(passwd_as_num, 11) ^ 1,
        "electric_suit": get_bit(passwd_as_num, 12) ^ 1,
        "symbiote_suit": get_bit(passwd_as_num, 16),
        "compressor": get_bit(passwd_as_num, 17),
        "fluid_upgrade": get_bit(passwd_as_num, 19),
        "heavy_impact": get_bit(passwd_as_num, 20),
        "difficulty": (
            move_bit(get_bit(passwd_as_num, 3) ^ 1, 0)
            | move_bit(get_bit(passwd_as_num, 9) ^ 1, 1)
        ),
        "empire_metals": get_bit(passwd_as_num, 14),
        "downtown": get_bit(passwd_as_num, 6) ^ 1,
        "pier_54": get_bit(passwd_as_num, 13),
        "chemcorp": get_bit(passwd_as_num, 4) ^ 1,
        "nightclub": get_bit(passwd_as_num, 22),
        "museum": get_bit(passwd_as_num, 8) ^ 1,
        "amusement_park": get_bit(passwd_as_num, 23),
    }


def encode(state):
    passwd_as_num = (
        move_bit(0, 0)
        | move_bit(state["belt"], 1)
        | move_bit(state["left_wrist"], 2)
        | move_bit(get_bit(state["difficulty"], 0) ^ 1, 3)
        | move_bit(state["chemcorp"] ^ 1, 4)
        | move_bit(0, 5)
        | move_bit(state["downtown"] ^ 1, 6)
        | move_bit(state["right_wrist"] ^ 1, 7)
        | move_bit(state["museum"] ^ 1, 8)
        | move_bit(get_bit(state["difficulty"], 1) ^ 1, 9)
        | move_bit(state["thermal_suit"] ^ 1, 10)
        | move_bit(state["armor_suit"] ^ 1, 11)
        | move_bit(state["electric_suit"] ^ 1, 12)
        | move_bit(state["pier_54"], 13)
        | move_bit(state["empire_metals"], 14)
        | move_bit(
            (get_bit(state["difficulty"], 0) | get_bit(state["difficulty"], 1)) ^ 1, 15
        )
        | move_bit(state["symbiote_suit"], 16)
        | move_bit(state["compressor"], 17)
        | move_bit(0, 18)
        | move_bit(state["fluid_upgrade"], 19)
        | move_bit(state["heavy_impact"], 20)
        | move_bit(0, 21)
        | move_bit(state["nightclub"], 22)
        | move_bit(state["amusement_park"], 23)
    )
    passwd_as_num = set_secondary_bits(passwd_as_num)
    return num_to_pw(passwd_as_num)


def set_secondary_bits(passwd_as_num):
    passwd_as_num = (
        passwd_as_num
        | move_bit(
            (
                get_bit(passwd_as_num, 1)
                ^ get_bit(passwd_as_num, 11)
                ^ get_bit(passwd_as_num, 20)
                ^ get_bit(passwd_as_num, 4)
                ^ get_bit(passwd_as_num, 3)
            ),
            0,
        )
        | move_bit(
            (
                get_bit(passwd_as_num, 2)
                ^ get_bit(passwd_as_num, 7)
                ^ get_bit(passwd_as_num, 20)
                ^ get_bit(passwd_as_num, 8)
                ^ get_bit(passwd_as_num, 15)
            ),
            5,
        )
        | move_bit(
            (
                get_bit(passwd_as_num, 10)
                ^ get_bit(passwd_as_num, 16)
                ^ get_bit(passwd_as_num, 20)
                ^ get_bit(passwd_as_num, 4)
                ^ get_bit(passwd_as_num, 15)
            ),
            18,
        )
    )
    passwd_as_num = (
        passwd_as_num
        | move_bit(
            (
                get_bit(passwd_as_num, 0)
                ^ get_bit(passwd_as_num, 12)
                ^ get_bit(passwd_as_num, 17)
                ^ get_bit(passwd_as_num, 23)
                ^ get_bit(passwd_as_num, 9)
            ),
            21,
        )
        | move_bit(
            (
                get_bit(passwd_as_num, 5)
                ^ get_bit(passwd_as_num, 18)
                ^ get_bit(passwd_as_num, 19)
                ^ get_bit(passwd_as_num, 6)
                ^ get_bit(passwd_as_num, 3)
            ),
            24,
        )
    )
    return passwd_as_num


def run_tests():
    print("Running tests...")
    assert pw_to_num("SP1DY") == 0x131596E
    assert num_to_pw(pw_to_num("ZV3Z0")) == "ZV3Z0"
    assert not check("BBBBB")
    assert not check("SP1DV")
    known_codes = [
        "080ZG",
        "4-KMD",
        "7V84Z",
        "C0-LQ",
        "CV-L1",
        "HV37K",
        "JV31-",
        "JV33R",
        "JV37H",
        "RV8WJ",
        "SP1DY",
        "TW3-K",
        "TW3-R",
        "VV-BG",
        "W70ZZ",
        "W7HV1",
        "W7HZZ",
        "Z787K",
        "ZV3Z0",
        "ZV7Z2",
        "ZV87K",
        "TB31T",
    ]
    for code in known_codes:
        assert check(code)
        assert encode(decode(code)) == code
    print("Tests passed!")


def to_bin(n):
    s = bin(n & 0b11111111)[2:]
    return ("{0:0>8}").format(s)


def get_bit(num, bit):
    return (num & (1 << bit)) >> bit


def move_bit(num, bit):
    return (num & 1) << bit


if __name__ == "__main__":
    run_tests()
