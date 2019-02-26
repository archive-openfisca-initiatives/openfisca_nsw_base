# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *


class active_kids__voucher_amount(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Calculates voucher amount for Active Kids"

    def formula(persons, period, parameters):
        return persons('active_kids__child_meets_criteria', period) \
            * parameters(period).active_kids.voucher


class active_kids__child_meets_criteria(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "child meets criteria for Active Kids"

    def formula(persons, period, parameters):
        min_age = parameters(period).active_kids.min_age
        max_age = parameters(period).active_kids.max_age
        age = persons('age_in_months', period)
        return (
            persons('is_nsw_resident', period) *
            persons('is_enrolled_full_time', period) *
            (age >= min_age) * (age < max_age)
            )


class active_kids__is_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "person is a parent/carer/guardian and is entitled to 1 or more Active Kids vouchers for their family"

    def formula(persons, period, parameters):
        parent = persons('is_parent', period)
        guardian = persons('is_guardian', period)
        carer = persons('is_carer', period)
        return (parent + guardian + carer) * persons.family('active_kids__family_has_children_eligible', period)


class active_kids__family_has_children_eligible(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "family has 1 or more children eligible for Active Kids vouchers"

    def formula(families, period, parameters):
        eligible = families.members('active_kids__child_meets_criteria', period)
        return families.any(eligible, role=Family.CHILD)
