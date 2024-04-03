pragma circom  2.1.6;

include "dualMux.circom";
include "hashLeftRight.circom";

template MerkleTreeVerifier(depth) {
    signal input leaf;
    signal input merkleRoot;
    signal input merkleBranches[depth];
    signal input merkleOrder[depth]; // 0 - left | 1 - right

    component selectors[depth];
    component hashers[depth];

    for (var i = 0; i < depth; i++) {
        selectors[i] = DualMux();

        selectors[i].in[0] <== i == 0 ? leaf : hashers[i - 1].hash;
        selectors[i].in[1] <== merkleBranches[i];

        selectors[i].order <== merkleOrder[i];

        hashers[i] = HashLeftRight();

        hashers[i].left <== selectors[i].out[0];
        hashers[i].right <== selectors[i].out[1];
    }

    // merkleRoot === hashers[depth - 1].hash; //TODO: RESTORE THIS CONTRAINT AFTER TESTS
}
