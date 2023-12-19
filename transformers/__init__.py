from .axiom_transformer import transform_sales as axiom_transform_sales
from .dubai_duty_transform import transform_sales as dubai_duty_transform_sales
from .eros_transformer import transform_sales as eros_transform_sales
from .e_city_transformer import transform_sales as ecity_transform_sales
from .Jackys_transformer import transform_sales as jackys_transform_sales
from .nesto_transformer import transform_sales as nesto_transform_sales
transform_sales_methods = {
    "axiom": axiom_transform_sales,
    "dubai_duty": dubai_duty_transform_sales,
    "eros": eros_transform_sales,
    "e_city": ecity_transform_sales,
    "jackys": jackys_transform_sales,
    "nesto_xiaomi" : nesto_transform_sales,
    "nesto_lazor" : nesto_transform_sales,
}



def transform_sales(key, x,source):
    return transform_sales_methods[key](x,source)