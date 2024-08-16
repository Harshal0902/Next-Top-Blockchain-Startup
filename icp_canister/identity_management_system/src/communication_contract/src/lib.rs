use ic_cdk::export::Principal;
use ic_cdk::storage;

#[derive(Default)]
struct CommunicationContract {
    messages: Vec<(Principal, String)>,
}

#[ic_cdk::update]
fn send_message(to: Principal, message: String) {
    let contract = storage::get_mut::<CommunicationContract>();
    contract.messages.push((to, message));
}

#[ic_cdk::query]
fn get_messages() -> Vec<(Principal, String)> {
    let contract = storage::get::<CommunicationContract>();
    contract.messages.clone()
}