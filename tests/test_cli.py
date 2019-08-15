from base64 import b64decode, b64encode
import fileinput
import json
import os
import pytest
from click.testing import CliRunner
from prio.cli import commands


@pytest.fixture
def shared_seed():
    runner = CliRunner()
    result = runner.invoke(commands.shared_seed)
    assert result.exit_code == 0
    return result.output


def _keygen():
    runner = CliRunner()
    result = runner.invoke(commands.keygen)
    assert result.exit_code == 0
    return json.loads(result.output)


@pytest.fixture
def keygen_server_a():
    return _keygen()


@pytest.fixture
def keygen_server_b():
    return _keygen()


def test_keygen(keygen_server_a):
    assert set(keygen_server_a.keys()) == set(["private_key", "public_key"])
    # CURVE25519_KEY_LEN_HEX == 64 bytes
    assert (
        len(keygen_server_a["private_key"]) == len(keygen_server_a["public_key"]) == 64
    )


def test_shared_seed(shared_seed):
    # PRG_SEED_LENGTH == AES_128_KEY_LENGTH == 16
    assert len(b64decode(shared_seed)) == 16


def test_aggregate_end_to_end(tmp_path, shared_seed, keygen_server_a, keygen_server_b):
    ###########################################################
    # setup
    ###########################################################
    batch_id = "test"
    client_data = [[1, 0, 0], [1, 1, 0], [1, 1, 1]]
    n_data = len(client_data)

    base_args = ["--n-data", n_data, "--batch-id", batch_id]
    server_a_args = [
        "--server-id",
        "A",
        "--private-key-hex",
        keygen_server_a["private_key"],
        "--shared-secret",
        shared_seed,
        "--public-key-hex-internal",
        keygen_server_a["public_key"],
        "--public-key-hex-external",
        keygen_server_b["public_key"],
    ]
    server_b_args = [
        "--server-id",
        "B",
        "--private-key-hex",
        keygen_server_b["private_key"],
        "--shared-secret",
        shared_seed,
        "--public-key-hex-internal",
        keygen_server_b["public_key"],
        "--public-key-hex-external",
        keygen_server_a["public_key"],
    ]

    def _validate_intermediate_output(*args):
        # this only validates the output has the expected form
        for filename in args:
            output_lines = [filename for filename in open(filename).readlines()]
            assert len(output_lines) == n_data
            for line in output_lines:
                assert set(json.loads(line).keys()) == set(["id", "payload"])

    (client_bucket_path, server_a_bucket_path, server_b_bucket_path) = [
        tmp_path.joinpath(path)
        for path in ["working/client", "working/server_a", "working_server_b"]
    ]
    (server_a_share_path, server_b_share_path) = [
        path.joinpath("raw") for path in (server_a_bucket_path, server_b_bucket_path)
    ]
    for path in (client_bucket_path, server_a_share_path, server_b_share_path):
        os.makedirs(path)

    data_filename = client_bucket_path.joinpath("data.ndjson")
    with open(data_filename, "w") as f:
        f.write("\n".join([json.dumps(row) for row in client_data]))

    ###########################################################
    # encode-shares
    ###########################################################
    (server_a_share_output_filename, server_b_share_output_filename) = [
        share_path.joinpath("data.ndjson")
        for share_path in (server_a_share_path, server_b_share_path)
    ]

    runner = CliRunner()
    result = runner.invoke(
        commands.encode_shares,
        base_args
        + [
            "--public-key-hex-internal",
            keygen_server_a["public_key"],
            "--public-key-hex-external",
            keygen_server_b["public_key"],
            "--input",
            data_filename,
            "--output-A",
            server_a_share_path,
            "--output-B",
            server_b_share_path,
        ],
    )
    assert result.exit_code == 0

    _validate_intermediate_output(
        server_a_share_output_filename, server_b_share_output_filename
    )

    ###########################################################
    # verify1
    ###########################################################
    (server_a_verify1_path, server_b_verify1_path) = [
        path.joinpath("intermediate", "external", "verify1")
        for path in (server_a_bucket_path, server_b_bucket_path)
    ]
    (server_a_verify1_output_filename, server_b_verify1_output_filename) = [
        path.joinpath(path, "data.ndjson")
        for path in (server_a_verify1_path, server_b_verify1_path)
    ]

    # server A
    os.makedirs(server_a_verify1_path)
    result = runner.invoke(
        commands.verify1,
        base_args
        + server_a_args
        + [
            "--input",
            server_a_share_output_filename,
            "--output",
            server_a_verify1_path,
        ],
    )
    assert result.exit_code == 0

    # server B
    os.makedirs(server_b_verify1_path)
    result = runner.invoke(
        commands.verify1,
        base_args
        + server_b_args
        + [
            "--input",
            server_b_share_output_filename,
            "--output",
            server_b_verify1_path,
        ],
    )
    assert result.exit_code == 0

    _validate_intermediate_output(
        server_a_verify1_output_filename, server_b_verify1_output_filename
    )

    ###########################################################
    # verify2
    ###########################################################
    (server_a_verify2_path, server_b_verify2_path) = [
        path.joinpath("intermediate", "external", "verify2")
        for path in (server_a_bucket_path, server_b_bucket_path)
    ]
    (server_a_verify2_output_filename, server_b_verify2_output_filename) = [
        path.joinpath("data.ndjson")
        for path in (server_a_verify2_path, server_b_verify2_path)
    ]

    # server A
    os.makedirs(server_a_verify2_path)
    result = runner.invoke(
        commands.verify2,
        base_args
        + server_a_args
        + [
            "--input",
            server_a_share_output_filename,
            "--input-internal",
            server_a_verify1_output_filename,
            "--input-external",
            server_b_verify1_output_filename,
            "--output",
            server_a_verify2_path,
        ],
    )
    assert result.exit_code == 0

    # server B
    os.makedirs(server_b_verify2_path)
    result = runner.invoke(
        commands.verify2,
        base_args
        + server_b_args
        + [
            "--input",
            server_b_share_output_filename,
            "--input-internal",
            server_b_verify1_output_filename,
            "--input-external",
            server_a_verify1_output_filename,
            "--output",
            server_b_verify2_path,
        ],
    )
    assert result.exit_code == 0

    _validate_intermediate_output(
        server_a_verify2_output_filename, server_b_verify2_output_filename
    )

    ###########################################################
    # aggregate
    ###########################################################
    (server_a_aggregation_path, server_b_aggregation_path) = [
        path.joinpath("intermediate", "external", "aggregate")
        for path in (server_a_bucket_path, server_b_bucket_path)
    ]
    (server_a_aggregation_output_filename, server_b_aggregation_output_filename) = [
        path.joinpath("data.ndjson")
        for path in (server_a_aggregation_path, server_b_aggregation_path)
    ]

    # server A
    os.makedirs(server_a_aggregation_path)
    result = runner.invoke(
        commands.aggregate,
        base_args
        + server_a_args
        + [
            "--input",
            server_a_share_output_filename,
            "--input-internal",
            server_a_verify2_output_filename,
            "--input-external",
            server_b_verify2_output_filename,
            "--output",
            server_a_aggregation_path,
        ],
    )
    assert result.exit_code == 0

    # server B
    os.makedirs(server_b_aggregation_path)
    result = runner.invoke(
        commands.aggregate,
        base_args
        + server_b_args
        + [
            "--input",
            server_b_share_output_filename,
            "--input-internal",
            server_b_verify2_output_filename,
            "--input-external",
            server_a_verify2_output_filename,
            "--output",
            server_b_aggregation_path,
        ],
    )
    assert result.exit_code == 0

    ###########################################################
    # publish
    ###########################################################
    (server_a_published_path, server_b_published_path) = [
        path.joinpath("processed")
        for path in (server_a_bucket_path, server_b_bucket_path)
    ]
    (server_a_published_output_filename, server_b_published_output_filename) = [
        path.joinpath("data.ndjson")
        for path in (server_a_published_path, server_b_published_path)
    ]

    # server A
    os.makedirs(server_a_published_path)
    result = runner.invoke(
        commands.publish,
        base_args
        + server_a_args
        + [
            "--input-internal",
            server_a_aggregation_output_filename,
            "--input-external",
            server_b_aggregation_output_filename,
            "--output",
            server_a_published_path,
        ],
    )
    assert result.exit_code == 0

    # server B
    os.makedirs(server_b_published_path)
    result = runner.invoke(
        commands.publish,
        base_args
        + server_b_args
        + [
            "--input-internal",
            server_b_aggregation_output_filename,
            "--input-external",
            server_a_aggregation_output_filename,
            "--output",
            server_b_published_path,
        ],
    )
    assert result.exit_code == 0

    for filename in (
        server_a_published_output_filename,
        server_b_published_output_filename,
    ):
        assert json.load(open(filename)) == [3, 2, 1]


def test_partial_success(tmp_path, shared_seed):
    key_a = _keygen()
    key_b = _keygen()
    key_c = _keygen()

    batch_id = "test"
    n_data = 3
    base_args = ["--n-data", n_data, "--batch-id", batch_id]

    runner = CliRunner()

    def encode(key_0, key_1, output_path):
        input_path = tmp_path / "tmp"
        with open(input_path, "w") as f:
            f.write(json.dumps([1, 0, 1]))

        result = runner.invoke(
            commands.encode_shares,
            base_args
            + [
                "--public-key-hex-internal",
                key_0["public_key"],
                "--public-key-hex-external",
                key_1["public_key"],
                "--input",
                input_path,
                "--output-A",
                output_path,
                "--output-B",
                tmp_path / "ignored",
            ],
        )
        assert result.exit_code == 0

    # generate two sets of data points with different pairs of keys
    out_0 = tmp_path / "out-0"
    out_1 = tmp_path / "out-1"
    out_full = tmp_path / "out"
    out_verify1 = tmp_path / "verify1"

    encode(key_c, key_a, out_0)
    encode(key_c, key_b, out_1)

    # concatenate the two files together
    with open(out_full, "w") as f_out, fileinput.input([out_0, out_1]) as f_in:
        for line in f_in:
            f_out.write(line)

    # run through verify 1 and check the total number of lines
    result = runner.invoke(
        commands.verify1,
        base_args
        + [
            "--server-id",
            "A",
            "--private-key-hex",
            key_c["private_key"],
            "--shared-secret",
            shared_seed,
            "--public-key-hex-internal",
            key_c["public_key"],
            "--public-key-hex-external",
            key_a["public_key"],
            "--input",
            out_full,
            "--output",
            out_verify1,
        ],
    )
    assert result.exit_code == 0

    with open(out_full, "r") as f:
        assert len(f.readlines()) == 2

    with open(out_verify1, "r") as f:
        assert len(f.readlines()) == 1
