# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect

from google.appengine.ext import ndb
from google.appengine.ext.ndb.google_imports import datastore_errors
import pytest
import snippets


@pytest.yield_fixture
def client(testbed):
    yield testbed

    for name, obj in inspect.getmembers(snippets):
        if inspect.isclass(obj) and issubclass(obj, ndb.Model):
            ndb.delete_multi(obj.query().iter(keys_only=True))


def test_create_sandy_with_keywords(client):
    result = snippets.create_sandy_with_keywords()
    assert type(result) == snippets.Account


def test_create_sandy_manually(client):
    result = snippets.create_sandy_manually()
    assert type(result) == snippets.Account


def test_create_with_type_error_in_constructor(client):
    with pytest.raises(datastore_errors.BadValueError):
        snippets.create_with_type_error_in_constructor()


def test_assign_with_type_error(client):
    with pytest.raises(datastore_errors.BadValueError):
        snippets.assign_with_type_error(snippets.create_sandy_with_keywords())


def test_store_sandy(client):
    result = snippets.store_sandy(snippets.create_sandy_with_keywords())
    assert type(result) == snippets.ndb.Key


def test_url_safe_sandy_key(client):
    sandy_key = snippets.store_sandy(snippets.create_sandy_with_keywords())
    result = snippets.url_safe_sandy_key(sandy_key)
    assert type(result) == str


def test_get_sandy_from_urlsafe(client):
    sandy_key = snippets.store_sandy(snippets.create_sandy_with_keywords())
    result = snippets.get_sandy_from_urlsafe(
        snippets.url_safe_sandy_key(sandy_key))
    assert type(result) == snippets.Account
    assert result.username == 'Sandy'


def test_id_from_urlsafe(client):
    sandy_key = snippets.store_sandy(snippets.create_sandy_with_keywords())
    urlsafe = snippets.url_safe_sandy_key(sandy_key)
    key, ident, kind_string = snippets.id_from_urlsafe(urlsafe)
    assert type(key) == ndb.Key
    assert type(ident) == long
    assert type(kind_string) == str


def test_update_key(client):
    sandy = snippets.create_sandy_with_keywords()
    sandy_key = snippets.store_sandy(sandy)
    urlsafe = snippets.url_safe_sandy_key(sandy_key)
    key, ident, kind_string = snippets.id_from_urlsafe(urlsafe)
    snippets.update_key(key)
    assert key.get().email == 'sandy@gmail.co.uk'


def test_delete_sandy(client):
    sandy = snippets.create_sandy_with_keywords()
    snippets.store_sandy(sandy)
    snippets.delete_sandy(sandy)
    assert sandy.key.get() is None


def test_create_sandy_named_key(client):
    result = snippets.create_sandy_named_key()
    assert 'SOME@WHERE.COM' == result


def test_set_key_directly(client):
    account = snippets.Account()
    snippets.set_key_directly(account)
    assert account.key.id() == 'SOME@WHERE.COM'


def test_create_sandy_with_generated_numeric_id(client):
    result = snippets.create_sandy_with_generated_numeric_id()
    assert type(result.key.id()) == long


def test_example_message_revisions(client):
    snippets.example_message_revisions()


def test_example_revision_equivalents(client):
    result = snippets.example_revision_equivalents()
    assert result.id() == 'sandy@foo.com'


def test_insert_message(client):
    result = snippets.insert_message()
    assert result.message_text == 'Hello'


def test_get_parent_key(client):
    initial_revision = snippets.insert_message()
    result = snippets.get_parent_key(initial_revision)
    assert result.kind() == 'Message'


def test_multi_key_ops(client):
    snippets.multi_key_ops([
        snippets.Account(email='a@a.com'), snippets.Account(email='b@b.com')])


def test_create_expando(client):
    result = snippets.create_expando()
    assert result.foo == 1


def test_expando_properties(client):
    result = snippets.expando_properties(snippets.create_expando())
    assert result['foo'] is not None
    assert result['bar'] is not None
    assert result['tags'] is not None


def test_create_flex_employee(client):
    result = snippets.create_flex_employee()
    assert result.name == 'Sandy'


def test_create_specialized(client):
    result = snippets.create_specialized()
    assert result['foo']
    assert result['bar']


def test_non_working_flex_query(client):
    with pytest.raises(AttributeError):
        snippets.non_working_flex_query()


def test_working_flex_employee(client):
    snippets.working_flex_employee()


def test_demonstrate_hook(client):
    iterator = snippets.demonstrate_hook()
    iterator.next()
    assert snippets.notification == 'Gee wiz I have a new friend!'
    iterator.next()
    assert snippets.notification == 'I suck and nobody likes me.'


def test_reserve_ids(client):
    first, last = snippets.reserve_ids()
    assert last - first >= 99


def test_reserve_ids_with_parent(client):
    first, last = snippets.reserve_ids_with_parent(snippets.Friend().key)
    assert last - first >= 99


def test_construct_keys(client):
    result = snippets.construct_keys(*snippets.reserve_ids())
    assert len(result) == 100


def test_reserve_ids_up_to(client):
    first, last = snippets.reserve_ids_up_to(5)
    assert last - first >= 4
