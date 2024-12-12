from .repo import Repo
from .motivation import Motivation
from .founder import Founder
from .validator import Validator
from .user import User

from faker import Faker

class Service:
    def __init__(self, repo:Repo):
        self.xrepo=repo
        self._last_id=0

    def _get_last_id(self):
        self._last_id+=1
        return self._last_id

    def add_faker_data(self, count=100000):
        fakerul=Faker()
        from random import randint
        for i in range(count):
            name=fakerul.color()+fakerul.country()+fakerul.color()
            strength=randint(0,5)
            # new_motivation=Motivation(0, name, strength)
            self.add({
                "id":0,
                "name":name,
                "strength":strength
            })
    def add_secondary_faker_data(self, count=100000):
        self.xrepo.add_secondary_faker_data(count)

    def commit_to_db(self):
        self.xrepo.commit_to_db()

    def add_examples(self):
        examples=[
            Motivation(0, "Kill Bill", 5),
            Motivation(1, "To be evil", 1),
            Motivation(2, "To be special", 4),
            Motivation(3, "Zumba", 5),
            Motivation(4, "Aesthetics madness", 5),
            Motivation(5, "Conquering Troy", 5)
        ]
        for x in examples:
            self.xrepo.add(x)

    def get(self, id):
        entity=self.xrepo.get(id)
        if entity is None:
            raise Exception("No entity with this id")
        return self.xrepo.get(id).to_dict()
    
    def get_by_name(self, name):
        all=self.xrepo.get_all()
        ans = list(filter(lambda x : x.name==name, all))
        if len(ans)==0:
            return None
        return ans[0].to_dict()

    def get_all(self):
        all=self.xrepo.get_all()
        return all
    
    def get_strenghts(self):
        return set([motivation.strength for motivation in self.xrepo.get_all()])

    def get_page(self, index, size, all=None):
        # page = self.xrepo.get_motivations_page(self, index, size)
        # return page,1,100
        if all is None:
            all=self.get_all()
        index=max(index,0)
        left_index=min(index*size, len(all)//size*size)
        right_index=min(left_index+size, len(all))
        page=all[left_index:right_index]
        max_len=len(all)//size+(1 if len(all)%size==0 else 0)
        return page,left_index//size,len(all)
    
    def get_founders_by_motivation_id(self, id):
        return self.xrepo.get_founders_by_motivation_id(id)

    def get_filter_page(self, index, size, name_filter_key=None, strength_filter_key=None, sort_by_name=False):
        def apply_filters(self,elements, filters):
            for my_filter in filters:
                elements=my_filter(self,elements)
            return elements
        def name_filter(self, all):
            return list(filter(lambda x : name_filter_key in x.name, all))
        def strength_filter(self, all):
            return list(filter(lambda x: abs(strength_filter_key- x.strength)<=0.99, all))
        def sort_by_name_filter(self, elements):
            return sorted(elements, key=lambda x : x.name)
        filters_list=[]
        if name_filter_key is not None:
            filters_list.append(name_filter)
        if strength_filter_key is not None:
            filters_list.append(strength_filter)
        if sort_by_name:
            print("sorted by name", sort_by_name)
            filters_list.append(sort_by_name_filter)
        elements=self.get_all()
        elements=apply_filters(self, elements, filters_list)
        return self.get_page(index, size, elements)

    def get_all_dict(self):
        all=self.get_all()
        return [x.to_dict() for x in all]

    def _validate_motivation(self, motivation):
        if not Motivation.is_valid(motivation):
            raise Exception("Motivation not valid")
        if self.get_by_name(motivation.name) is not None:
            raise Exception("Motivation name must be unique")

    def add(self, entity_json):
        new_motivation=Motivation.from_dict(entity_json)
        new_motivation.id=self._get_last_id()
        Validator.validate(new_motivation)
        self.xrepo.add(new_motivation)
        return new_motivation.to_dict()

    def remove(self, id):
        if self.xrepo.get(id) is None :
            raise Exception("Id"+str(id)+" not found for deletion")
        self.xrepo.remove(id)

    def update(self, id, entity_json):
        if self.xrepo.get(id) is None :
            raise Exception("Id not found for update")
        self.xrepo.remove(id)
        new_motivation=Motivation.from_dict(entity_json)
        new_motivation.id=id
        self._validate_motivation(new_motivation)
        self.xrepo.add(new_motivation)
        return new_motivation

    def founder_add(self, motivation_id, name, email):
        new_founder=Founder(name, email, motivation_id)
        self.xrepo.add(new_founder)

    def founder_remove(self, id):
        self.xrepo.founder_remove(id)

    def founder_update(self, id , motivation_id, name, email):
        new_founder=Founder(name, email, motivation_id)
        self.xrepo.founder_update(id, new_founder)

    def founder_get(self, id):
        founder = self.xrepo.founder_get(id)
        return {
            "name":founder.name,
            "email":founder.email,
        }

    def founder_get_all(self):
        return self.xrepo.founder_get_all()


    def user_add(self, username, user_type, is_active, password):
        new_user = User(username, user_type, is_active, password)
        self.xrepo.add(new_user)
    
    def user_remove(self, id):
        self.xrepo.user_remove(id)

    def user_update(self, id, username, user_type, is_active, password):
        updated_user = User(username, user_type, is_active, password)
        self.xrepo.user_update(id, updated_user)

    def user_get(self, id):
        user = self.xrepo.user_get(id)
        return {
            "username": user.username,
            "email": user.email,
        }

    def get_all_users(self, page=1, per_page=10):
        return self.xrepo.get_all_users(page, per_page)