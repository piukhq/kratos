class Givex911Response():
    transaction_code: str
    result: str
    givex_transaction_reference: str
    error_message: str
    points_added: str
    points_balance: str
    certificate_balance: str
    member_name: str
    receipt_message: str
    discount_amount: str
    iso_serial: str
    unit_balance: str
    loyalty_balance: str
    certificate_expiration_date: str
    transaction_code: str
    result: str
    givex_transaction_reference: str
    error_message: str
    points_added: str
    points_balance: str
    certificate_balance: str
    member_name: str
    receipt_message: str
    discount_amount: str
    iso_serial: str
    unit_balance: str
    loyalty_balance: str
    certificate_expiration_date: str 

    def __init__(self, input_array ):
        self.transaction_code = input_array[0]
        self.result = input_array[1]
        if self.result == '0':
            self.givex_transaction_reference = input_array[2]
            self.points_added = input_array[3]
            self.points_balance = input_array[4]
            self.certificate_balance = input_array[5]
            self.member_name = input_array[6]
            self.receipt_message = input_array[7]
            self.discount_amount = input_array[8]
            self.iso_serial = input_array[9]
            self.unit_balance = input_array[10]
            self.loyalty_balance = input_array[11]
            self.certificate_expiration_date = input_array[12]
        else:  
            self.error_message = input_array[2]

class Givex945Response():
    transaction_code: str
    result: str
    error_message: str
    givex_transaction_reference: str
    points_removed: str
    points_balance: str
    iso_serial: str    

    def __init__(self, input_array: list ):
        self.transaction_code = input_array[0]
        self.result = input_array[1]
        if self.result == '0':
            self.givex_transaction_reference = input_array[2]
            self.points_removed = input_array[3]
            self.points_balance = input_array[4]
        else: 
            self.error_message = input_array[2]

class Givex946Response():
    transaction_code: str
    result: str
    error_message: str
    customer_id: str
    customer_first_name: str
    customer_last_name: str
    customer_reg_date: str
    iso_serial: str
    loyalty_enroll_id: str
    login_token: str
    customer_reference: str
    otp_key: str
    otp_url: str
    email_verification_status: str    

    def __init__(self, input_array: list ):
        self.transaction_code = input_array[0]
        self.result = input_array[1]
        if self.result == '0':
            self.customer_id = input_array[2]
            self.customer_first_name = input_array[3]
            self.customer_last_name = input_array[4]
            self.customer_reg_date = input_array[5]
            self.iso_serial = input_array[6]
            self.loyalty_enroll_id = input_array[7]
            self.login_token = input_array[8]
            self.customer_reference = input_array[9]
        else: 
            self.error_message = input_array[2]

class Givex995Response():
    transaction_code: str
    result: str
    error_message: str
    certificate_balance: str
    currency: str
    points_balance: str
    transhist: list = []
    totalrows: str
    iso_serial: str
    certificate_expiration_date: str
    operator_message: str

    def transform_transhist(self, input_array: list):
        transaction_history_record = []
        transaction_history_record.append(vars(PointsTransaction(input_array)))
        return transaction_history_record

    def __init__(self, input_array:str ):
        self.transaction_code = input_array[0]
        self.result = input_array[1]
        if self.result == '0':
            self.certificate_balance = input_array[2]
            self.currency = input_array[3]
            self.points_balance = input_array[4]
            transaction_history_list = []
            for i in input_array[5]:
                 transaction_history_list.append(self.transform_transhist(i))
#            self.transhist = input_array[5]
            self.transhist = transaction_history_list
            self.totalrows = input_array[6]
            self.iso_serial = input_array[7]
            self.certificate_expiration_date = input_array[8]
            self.operator_message = input_array[9]
        else: 
            self.error_message = input_array[2]

class Givex996Response():
    transaction_code: str
    result: str
    error_message: str
    member_address: str
    member_mobile: str
    member_email: str
    member_birthdate: str
    sms_contact_number: str
    email_contact_answer: str
    mail_contact_answer: str
    member_phone: str
    referring_member_name: str
    member_title: str
    iso_serial: str
    purchase_amount_to_next_tier: str
    purchase_amount_email_curreny_tier: str
    purchase_amount_via_default_promo_code: str
    date_of_the_last_tier_change: str
    amount_spent_since_last_tier_change: str
    message_type: str
    message_delivery_method: str
    points_to_earn_to_reach_next_tier: str
    points_to_earn_to_remain_in_current_tier: str
    total_points_earned_since_last_upgrade: str
    next_points_to_money_automatic_conversion_threshold: str
    points_required_for_next_points_to_money_automatic_conversion: str
    tier_id: str
    tier_name: str

    def __init__(self, input_array ):
        self.transaction_code = input_array[0]
        self.result = input_array[1]
        if self.result == '0':
            self.member_address = input_array[2]
            self.member_mobile = input_array[3]
            self.member_email = input_array[4]
            self.member_birthdate = input_array[5]
            self.sms_contact_number = input_array[6]
            self.email_contact_answer = input_array[7]
            self.mail_contact_answer = input_array[8]
            self.member_phone = input_array[9]
            self.referring_member_name = input_array[10]
            self.member_title = input_array[11]
            self.iso_serial = input_array[12]
            self.purchase_amount_to_next_tier = input_array[13]
            self.purchase_amount_email_curreny_tier = input_array[14]
            self.purchase_amount_via_default_promo_code = input_array[15]
            self.date_of_the_last_tier_change = input_array[16]
            self.amount_spent_since_last_tier_change = input_array[17]
            self.message_type = input_array[18]
            self.message_delivery_method = input_array[19]
            self.points_to_earn_to_reach_next_tier = input_array[20]
            self.points_to_earn_to_remain_in_current_tier = input_array[21]
            self.total_points_earned_since_last_upgrade = input_array[22]
            self.next_points_to_money_automatic_conversion_threshold = input_array[23]
        else:  
            self.error_message = input_array[2]

class PointsTransaction():
    transaction_local_date: str
    transaction_local_time: str
    transaction_type: str
    points: str
    store_name: str
    points_amount: str
    pointsskudetail_element: list
    transaction_id: str
    channel_id: str
    transaction_server_datetime: str
    visit_datetime: str
    transaction_type_id: str
    operator: str
    store_user: str
    promo_code: str
    base_points: str
    tier_bonus_points: str
    promo_code_points: str
    tier_id: str
    transaction_ref: str
    merchant_ref: str 
    
    def __init__(self, input_array: list ):
        self.transaction_local_date = input_array[0]
        self.transaction_local_time = input_array[1]
        self.transaction_type = input_array[2]
        self.points = input_array[3]
        self.store_name = input_array[4]
        self.points_amount = input_array[5]
        self.pointsskudetail_element = input_array[6]
        self.transaction_id = input_array[7]
        self.channel_id = input_array[8]
        self.transaction_server_datetime = input_array[9]
        self.visit_datetime = input_array[10]
        self.transaction_type_id = input_array[11]
        self.operator = input_array[12]
        self.store_user = input_array[13]
        self.promo_code = input_array[14]
        self.base_points = input_array[15]
        self.tier_bonus_points = input_array[16]
        self.promo_code_points = input_array[17]
        self.tier_id = input_array[18]