
pragma circom  2.1.6;

include "./circuits/registerIdentityUniversal.circom";

// pub signals:
// [0]  -  dg15PubKeyHash
// [1]  -  dg1Commitment
// [2]  -  pkIdentityHash
// [3]  -  slaveMerkleRoot
component main { public [slaveMerkleRoot] } = RegisterIdentityUniversal(64, 32, 17, 4, 80, 760);
