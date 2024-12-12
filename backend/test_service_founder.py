
import unittest
from backhand.cruds.service import Service
from backhand.cruds.repo import Repo
from backhand.cruds.motivation import Motivation
from backhand.cruds.founder import Founder

from backhand import db
from backhand import create_app


app=create_app()


with app.app_context():
    class RepoTests(unittest.TestCase):
        def setUp(self):
            self.repo=Repo(db)
            self.examples=[
                Motivation(0, "zKill Bill", 5),
                Motivation(1, "To be evil", 1),
                Motivation(2, "aTo be special", 4)
            ]
            self.new_examples=[
                Motivation(3, "To win", 5),
                Motivation(4, "To not lose", 1),
                Motivation(5, "To be yourself", 4)
            ]
            for x in self.examples:
                self.repo.add(x)

        def tearDown(self):
            for x in self.examples:
                self.repo.remove(x._id)
            for x in self.new_examples:
                self.repo.remove(x._id)

        def test_get(self):
            self.assertEqual(self.repo.get(1234), None)
        
        def test_get_all(self):
            result=self.repo.get_all()
            self.assertEqual(result, self.examples)
        
        def test_add(self):
            ids=[]
            for x in self.new_examples:
                self.repo.add(x)
            for x in self.new_examples:
                self.assertTrue((self.repo.get(x._id) is not None))

        def test_remove(self):
            x=self.examples[0]
            self.repo.remove(x._id)
            self.assertTrue( self.repo.get(x._id) is None )

    def run():
        unittest.main()

    if __name__=="__main__":
        run()


# class ServiceTests(unittest.TestCase):
    class ServiceTests(unittest.TestCase):

        def setUp(self):
            # self.repo=Repo(db)
            repo=Repo(db)
            self.examples=[
                Motivation(0, "zKill Bill", 5),
                Motivation(1, "To be evil", 1),
                Motivation(2, "aTo be special", 4)
            ]
            self.new_examples=[
                Motivation(3, "To win", 5),
                Motivation(4, "To not lose", 1),
                Motivation(5, "To be yourself", 4)
            ]
            for x in self.examples:
                repo.add(x)
            self.service=Service(repo)

        def tearDown(self):
            for x in self.examples:
                self.repo.remove(x._id)
            for x in self.new_examples:
                self.repo.remove(x._id)

        def test_get(self):
            for i in range(len(self.examples)):
                x=self.examples[i]
                result=self.service.get(x.id)
                self.assertEqual(result, x.to_dict())
            try:
                self.service.get(123)
                self.assertTrue(False)
            except Exception as e:
                self.assertTrue(True)
        
        def test_get_all(self):
            result=self.service.get_all()
            self.assertEqual(result, self.examples)
        
        def test_add(self):
            ids=[]
            for x in self.new_examples:
                new_motivation=self.service.add(x.to_dict())
                ids.append(new_motivation["id"])

            for id in ids:
                try:
                    self.service.get(id)
                except Exception:
                    self.assertFalse(True)

        def test_remove(self):
            x=self.examples[0]
            self.service.remove(x.id)
            try:
                self.service.get(x.id)
                self.assertTrue(False)
            except:
                self.assertTrue(True)
            try:
                self.service.remove(7346)
                self.assertTrue(False)
            except:
                self.assertTrue(True)

        def test_update(self):
            x=self.examples[0]
            y=self.new_examples[0]
            self.service.update(x.id, y.to_dict())
            updated=self.service.get(x.id)
            y.id=x.id
            self.assertEqual(y.to_dict(), updated)

        def test_sorting_name(self):
            examples_order=sorted( 
                self.examples,
                key=lambda x : x.name
            )
            result=self.service.get_sorted_by_name()
            for i in range(len(examples_order)):
                self.assertEqual( result[i], examples_order[i].to_dict())
