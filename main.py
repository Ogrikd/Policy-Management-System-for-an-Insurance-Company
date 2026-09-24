from policy import *
from payment import *
from products import *

policy_manager = PolicyManager()
payment_manager = PaymentManager()
product_manager = ProductManager()

health_plan = product_manager.create_product(1, "Health Plan", 5000, "Basic health cover")

holder1 = policy_manager.register("Ada Obi", 1)
p1 = payment_manager.create_payment(1, health_plan.product_id, health_plan.premium, "2026-10-01")
payment_manager.process_payment(p1)

holder2 = policy_manager.register("Musa Bello", 2)
p2 = payment_manager.create_payment(2, health_plan.product_id, health_plan.premium, "2026-10-15")
payment_manager.process_payment(p2)

holder1.display_details(payment_manager, product_manager)
holder2.display_details(payment_manager, product_manager)

# Persist everything
policy_manager.save_to_csv()
payment_manager.save_to_csv()
product_manager.save_to_csv()