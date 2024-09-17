pragma circom 2.1.6;

include  "../../../../circuits/identityManagement/circuits/registerIdentityBuilder.circom";

component main = RegisterIdentityBuilder(
		2,
		8,
		8,
		8,
		512,
		256,	//hash type
		1,
		0,
		17,
		64,
		32,
		256,
		1,
		80,
		[[232, 1480, 336, 5, 4, 1]],
		1,
		[
			[0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 0, 1, 0, 0, 0, 0],
			[0, 1, 0, 0, 0, 0, 0, 0]
		]
);