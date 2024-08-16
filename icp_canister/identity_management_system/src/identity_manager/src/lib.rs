use ic_cdk::export::Principal;
use ic_cdk::storage;
use std::collections::HashMap;

#[derive(Default)]
struct IdentityManager {
    identities: HashMap<Principal, String>,
}

#[ic_cdk::update]
fn register_identity(identity: String) {
    let caller = ic_cdk::api::caller();
    let manager = storage::get_mut::<IdentityManager>();
    manager.identities.insert(caller, identity);
}

#[ic_cdk::query]
fn get_identity() -> Option<String> {
    let caller = ic_cdk::api::caller();
    let manager = storage::get::<IdentityManager>();
    manager.identities.get(&caller).cloned()
}