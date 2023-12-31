-- Setup database schema for testing

-- Data for Name: user; Type: TABLE DATA; Schema: public
INSERT INTO public."user"
    ("subject", "issuer", "created", "modified")
VALUES
    ('user_1',	'issuer_1',	'2000-01-01 00:00:00.000',	'2000-01-01 00:00:00.000'),
    ('user_2',	'issuer_1',	'2000-01-01 00:00:00.000',	'2000-01-01 00:00:00.000');


-- Data for Name: template; Type: TABLE DATA; Schema: public
INSERT INTO public."template"
    ("id", "created", "modified", "repoFile", "title", "summary", "score", "picture", "gitLink", "feedback", "gitCheckout")
VALUES
    ('bced037a-a326-425d-aa03-5d3cbc9aa3d1',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'my_template_1.json',			'My Template 1',		'Tests Cookiecutter',   5.0,	'path/to/picture.png',	'https://link-to-be-patched',   'https://link-to-feedback',   'main'),
    ('ef231acb-0ff9-4391-ab18-6cb2698b0985',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'my_template_2.json',			'My Template 2',		'Basic Cookiecutter',	null,   'path/to/picture.png',	'https://github.com/BruceEckel/HelloCookieCutter1',   'https://link-to-feedback',	'master'),
    ('8fc20f81-e0a9-471c-8008-697ce799e73b',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'my_template_3.json',			'My Template 3',		'Template example 3',	4.5,   'path/to/picture.png',	'https://some-git-link/template',   'https://link-to-feedback',	'main'),
    ('f3f35224-e35c-46a4-90d1-354646970b13',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'my_template_4.json',			'My Template 4',		'Template example 4',	null,   'path/to/picture.png',	'https://some-git-link/template',   'https://link-to-feedback',	'main'),
    ('eebb17f2-1f25-431d-94bf-b3561d8b4758',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'deephdc-master.json',			'DEEP-HDC',				'Template for developing new modules in the DEEP Platform',	null,	'wp-content/uploads/sites/2/2018/01/logo.png',	'https://github.com/deephdc/cookiecutter-deep',   'https://link-to-feedback',	'master'),
    ('479b4f69-9760-44d9-8018-b3077d0b5416',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'deephdc-child-module.json',	'DEEP-HDC Child',		'Template for developing new modules in the DEEP Platform, tailored for users performing a retraining of an existing module',	null,   'wp-content/uploads/sites/2/2018/01/logo.png',	'https://github.com/deephdc/cookiecutter-deep',   'https://link-to-feedback',	'child-module'),
    ('508515f1-dd27-4198-b8c3-3109b8bc06bc',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'deephdc-advanced.json',		'DEEP-HDC Advanced',	'Template for developing new modules in the DEEP Platform, makes more assumptions on how to structure projects and adds more files than those strictly needed for integration',	null,	'wp-content/uploads/sites/2/2018/01/logo.png',	'https://github.com/deephdc/cookiecutter-deep',   'https://link-to-feedback',	'advanced');


-- Data for Name: tag; Type: TABLE DATA; Schema: public
INSERT INTO public."tag"
    ("id", "name")
VALUES
    ('b6f056df-9416-4832-ac0a-4966d9c2a4d5',	'python'),
    ('7aa6e35a-bd97-4478-9244-6856a5062ff9',	'rust'),
    ('94df322b-2975-4692-9744-5fc9e4d0032c',	'erlang');



-- Data for Name: tag_association; Type: TABLE DATA; Schema: public
INSERT INTO public."tag_association"
    ("template_id", "tag_id")
VALUES
    ('bced037a-a326-425d-aa03-5d3cbc9aa3d1',	'b6f056df-9416-4832-ac0a-4966d9c2a4d5'),
    ('bced037a-a326-425d-aa03-5d3cbc9aa3d1',	'7aa6e35a-bd97-4478-9244-6856a5062ff9'),
    ('ef231acb-0ff9-4391-ab18-6cb2698b0985',	'b6f056df-9416-4832-ac0a-4966d9c2a4d5'),
    ('8fc20f81-e0a9-471c-8008-697ce799e73b',	'94df322b-2975-4692-9744-5fc9e4d0032c');


-- Data for Name: score; Type: TABLE DATA; Schema: public
INSERT INTO public."score"
    ("id", "created", "modified", "parent_id", "value", "owner_subject", "owner_issuer")
VALUES
    ('fbd43094-2e38-4cb8-a2ac-043950016168',	'2000-01-01 00:00:00.000',	'2000-01-01 00:00:00.000',	'bced037a-a326-425d-aa03-5d3cbc9aa3d1',	5.0,	'user_1',	'issuer_1'),
    ('19f312d5-2947-4c6f-8fa0-27c77173cfa4',	'2000-01-01 00:00:00.000',	'2000-01-01 00:00:00.000',	'8fc20f81-e0a9-471c-8008-697ce799e73b',	4.0,	'user_1',	'issuer_1'),
    ('3b560633-110a-453d-9345-0781126e76bf',	'2000-01-01 00:00:00.000',	'2000-01-01 00:00:00.000',	'8fc20f81-e0a9-471c-8008-697ce799e73b',	5.0,	'user_2',	'issuer_1');
