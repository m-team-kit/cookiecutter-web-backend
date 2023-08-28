-- Setup database schema for testing

-- Data for Name: user; Type: TABLE DATA; Schema: public
INSERT INTO public."user"
    ("subject", "issuer", "created", "modified")
VALUES
    ('user_1', 'issuer_1', '2000-01-01 00:00:00.000', '2000-01-01 00:00:00.000'),
    ('user_2', 'issuer_1', '2000-01-01 00:00:00.000', '2000-01-01 00:00:00.000');


-- Data for Name: template; Type: TABLE DATA; Schema: public
INSERT INTO public."template"
    ("id", "created", "modified", "repoFile", "title", "summary", "language", "picture", "gitLink", "gitCheckout")
VALUES
    ('bced037a-a326-425d-aa03-5d3cbc9aa3d1',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'my_template_1.json',	'HelloCookieCutter1',	'Cookiecutter basics',	'Python',	'https://picture-url/template_1',	'https://github.com/BruceEckel/HelloCookieCutter1',	'master'),
    ('ef231acb-0ff9-4391-ab18-6cb2698b0985',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'my_template_2.json',	'My Template 2',	'Template example 2',	'Python',	'https://picture-url/template_2',	'https://some-git-link/template_2',	'main'),
    ('8fc20f81-e0a9-471c-8008-697ce799e73b',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'my_template_3.json',	'My Template 3',	'Template example 3',	'Python',	'https://picture-url/template_3',	'https://some-git-link/template_3',	'main'),
    ('f3f35224-e35c-46a4-90d1-354646970b13',	'2000-01-01 00:00:00.000',	'2020-01-01 00:00:000',	'my_template_4.json',	'My Template 4',	'Template example 4',	'Python',	'https://picture-url/template_4',	'https://some-git-link/template_4',	'main');


-- Data for Name: tag; Type: TABLE DATA; Schema: public
INSERT INTO public."tag"
    ("id", "parent_id", "name")
VALUES
    ('b6f056df-9416-4832-ac0a-4966d9c2a4d5',  'bced037a-a326-425d-aa03-5d3cbc9aa3d1',	'Tag1'),
    ('7aa6e35a-bd97-4478-9244-6856a5062ff9',  'bced037a-a326-425d-aa03-5d3cbc9aa3d1',	'Tag2'),
    ('9d85fb5d-ec9e-448f-9aaf-27f7dcdf5599',  'ef231acb-0ff9-4391-ab18-6cb2698b0985',	'Tag2'),
    ('94df322b-2975-4692-9744-5fc9e4d0032c',  '8fc20f81-e0a9-471c-8008-697ce799e73b',	'Tag3');


-- Data for Name: score; Type: TABLE DATA; Schema: public
INSERT INTO public."score"
    ("id", "created", "modified", "parent_id", "value", "owner_subject", "owner_issuer")
VALUES
    ('fbd43094-2e38-4cb8-a2ac-043950016168',  '2000-01-01 00:00:00.000',  '2000-01-01 00:00:00.000',  'bced037a-a326-425d-aa03-5d3cbc9aa3d1',  5.0,  'user_1',  'issuer_1'),
    ('19f312d5-2947-4c6f-8fa0-27c77173cfa4',  '2000-01-01 00:00:00.000',  '2000-01-01 00:00:00.000',  'bced037a-a326-425d-aa03-5d3cbc9aa3d1',  4.0,  'user_2',  'issuer_1'),
    ('3b560633-110a-453d-9345-0781126e76bf',  '2000-01-01 00:00:00.000',  '2000-01-01 00:00:00.000',  'ef231acb-0ff9-4391-ab18-6cb2698b0985',  5.0,  'user_1',  'issuer_1');
