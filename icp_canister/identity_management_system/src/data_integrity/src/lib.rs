use ic_cdk::storage;

#[derive(Default)]
struct DataIntegrity {
    data_records: Vec<String>,
}

#[ic_cdk::update]
fn add_data_record(record: String) {
    let integrity = storage::get_mut::<DataIntegrity>();
    integrity.data_records.push(record);
}

#[ic_cdk::query]
fn get_data_records() -> Vec<String> {
    let integrity = storage::get::<DataIntegrity>();
    integrity.data_records.clone()
}