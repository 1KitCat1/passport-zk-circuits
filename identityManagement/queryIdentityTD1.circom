pragma circom  2.1.6;

include "./circuits/queryIdentityTD1.circom";

component main { public [eventID, 
                        eventData, 
                        idStateRoot, 
                        selector, 
                        timestampLowerbound,
                        timestampUpperbound,
                        identityCounterLowerbound,
                        identityCounterUpperbound,
                        birthDateLowerbound,
                        birthDateUpperbound,
                        expirationDateLowerbound,
                        expirationDateUpperbound,
                        citizenshipMask
                        ] } = QueryIdentity(80);