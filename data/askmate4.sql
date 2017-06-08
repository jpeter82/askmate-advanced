--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.7
-- Dumped by pg_dump version 9.5.7

-- Started on 2017-06-08 10:44:20 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE askmate;
--
-- TOC entry 2232 (class 1262 OID 16891)
-- Name: askmate; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE askmate WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


\connect askmate

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12395)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2234 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 194 (class 1255 OID 33107)
-- Name: update_reputation(integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION update_reputation(id integer, category character varying) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE volume integer;
BEGIN
	SELECT points INTO volume
	FROM reputation r
	WHERE r.category = update_reputation.category;
	
	UPDATE users u
	SET reputation = reputation + volume
	WHERE u.id = update_reputation.id;
	RETURN FOUND;
END;
$$;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 184 (class 1259 OID 24619)
-- Name: answer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE answer (
    id integer NOT NULL,
    submission_time timestamp without time zone DEFAULT date_trunc('second'::text, now()),
    vote_number integer DEFAULT 0,
    question_id integer DEFAULT 0,
    message text,
    image text,
    answered_by integer NOT NULL,
    accepted_by integer
);


--
-- TOC entry 183 (class 1259 OID 24617)
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2235 (class 0 OID 0)
-- Dependencies: 183
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE answer_id_seq OWNED BY answer.id;


--
-- TOC entry 186 (class 1259 OID 24631)
-- Name: comment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone DEFAULT date_trunc('second'::text, now()),
    edited_count integer DEFAULT 0,
    user_id integer NOT NULL
);


--
-- TOC entry 185 (class 1259 OID 24629)
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2236 (class 0 OID 0)
-- Dependencies: 185
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE comment_id_seq OWNED BY comment.id;


--
-- TOC entry 182 (class 1259 OID 24607)
-- Name: question; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE question (
    id integer NOT NULL,
    submission_time timestamp without time zone DEFAULT date_trunc('second'::text, now()),
    view_number integer DEFAULT 0,
    vote_number integer DEFAULT 0,
    title text,
    message text,
    image text,
    user_id integer
);


--
-- TOC entry 181 (class 1259 OID 24605)
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE question_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2237 (class 0 OID 0)
-- Dependencies: 181
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE question_id_seq OWNED BY question.id;


--
-- TOC entry 187 (class 1259 OID 24640)
-- Name: question_tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


--
-- TOC entry 193 (class 1259 OID 33098)
-- Name: reputation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE reputation (
    id integer NOT NULL,
    category character varying(100) NOT NULL,
    points integer NOT NULL,
    created timestamp without time zone DEFAULT date_trunc('second'::text, now())
);


--
-- TOC entry 192 (class 1259 OID 33096)
-- Name: reputation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE reputation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2238 (class 0 OID 0)
-- Dependencies: 192
-- Name: reputation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE reputation_id_seq OWNED BY reputation.id;


--
-- TOC entry 189 (class 1259 OID 24645)
-- Name: tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE tag (
    id integer NOT NULL,
    name text
);


--
-- TOC entry 188 (class 1259 OID 24643)
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2239 (class 0 OID 0)
-- Dependencies: 188
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE tag_id_seq OWNED BY tag.id;


--
-- TOC entry 191 (class 1259 OID 33066)
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE users (
    id integer NOT NULL,
    user_name character varying(50),
    reputation integer DEFAULT 0,
    reg_time timestamp without time zone DEFAULT date_trunc('second'::text, now())
);


--
-- TOC entry 190 (class 1259 OID 33064)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2240 (class 0 OID 0)
-- Dependencies: 190
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- TOC entry 2062 (class 2604 OID 24622)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY answer ALTER COLUMN id SET DEFAULT nextval('answer_id_seq'::regclass);


--
-- TOC entry 2066 (class 2604 OID 24634)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY comment ALTER COLUMN id SET DEFAULT nextval('comment_id_seq'::regclass);


--
-- TOC entry 2058 (class 2604 OID 24610)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY question ALTER COLUMN id SET DEFAULT nextval('question_id_seq'::regclass);


--
-- TOC entry 2073 (class 2604 OID 33101)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY reputation ALTER COLUMN id SET DEFAULT nextval('reputation_id_seq'::regclass);


--
-- TOC entry 2069 (class 2604 OID 24648)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY tag ALTER COLUMN id SET DEFAULT nextval('tag_id_seq'::regclass);


--
-- TOC entry 2070 (class 2604 OID 33069)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- TOC entry 2218 (class 0 OID 24619)
-- Dependencies: 184
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO answer (id, submission_time, vote_number, question_id, message, image, answered_by, accepted_by) VALUES (1, '2017-04-28 16:49:00', 4, 1, 'You need to use brackets: my_list = []', NULL, 1, NULL);
INSERT INTO answer (id, submission_time, vote_number, question_id, message, image, answered_by, accepted_by) VALUES (2, '2017-04-25 14:42:00', 35, 1, 'Look it up in the Python docs', 'images/image2.jpg', 1, NULL);
INSERT INTO answer (id, submission_time, vote_number, question_id, message, image, answered_by, accepted_by) VALUES (3, '2017-05-26 06:52:05', 6, 3, 'mfwmnvrekmnkjr', NULL, 1, NULL);


--
-- TOC entry 2241 (class 0 OID 0)
-- Dependencies: 183
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('answer_id_seq', 3, true);


--
-- TOC entry 2220 (class 0 OID 24631)
-- Dependencies: 186
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (1, 1, NULL, 'Question 1 Comment1', '2017-06-07 20:14:23', 0, 1);
INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (3, 1, NULL, 'Question 1 Comment3', '2017-06-07 20:14:23', 0, 1);
INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (2, 1, NULL, 'Question 1 Comment2', '2017-06-07 20:14:23', 0, 2);
INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (4, NULL, 1, 'Answer 1 Comment1', '2017-06-07 21:13:54', 0, 1);
INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (5, NULL, 2, 'Answer2 Comment1', '2017-06-07 21:13:54', 0, 3);
INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (6, NULL, 1, 'Answer 1 Comment2', '2017-06-07 21:13:54', 0, 2);
INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (7, NULL, 2, 'Answer2 Comment2', '2017-06-07 21:13:54', 0, 1);


--
-- TOC entry 2242 (class 0 OID 0)
-- Dependencies: 185
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('comment_id_seq', 7, true);


--
-- TOC entry 2216 (class 0 OID 24607)
-- Dependencies: 182
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image, user_id) VALUES (1, '2017-04-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'images/image1.png', 1);
INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image, user_id) VALUES (2, '2017-05-01 10:41:00', 1366, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', NULL, 1);
INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image, user_id) VALUES (6, '2017-06-05 16:52:44', 0, 0, '4th Question', 'gweigneiqdmqeindqi', NULL, 1);
INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image, user_id) VALUES (3, '2017-05-26 06:17:38', 18, 8, 'First question', 'Question BODY
gkorekgrwkgkr222', NULL, 2);
INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image, user_id) VALUES (4, '2017-06-05 16:52:44', 0, 0, '2nd Question', 'Qustion body foewijiwj', NULL, 2);
INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image, user_id) VALUES (5, '2017-06-05 16:52:44', 0, 0, '3rd Question', 'twmktmwkmtgkwmgkwm', NULL, 2);
INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image, user_id) VALUES (0, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL, 3);
INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image, user_id) VALUES (7, '2017-06-08 00:39:40', 0, 0, 'This is a title for a question', 'Message of the latest question', NULL, 3);


--
-- TOC entry 2243 (class 0 OID 0)
-- Dependencies: 181
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('question_id_seq', 9, true);


--
-- TOC entry 2221 (class 0 OID 24640)
-- Dependencies: 187
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO question_tag (question_id, tag_id) VALUES (0, 1);
INSERT INTO question_tag (question_id, tag_id) VALUES (1, 3);
INSERT INTO question_tag (question_id, tag_id) VALUES (2, 3);


--
-- TOC entry 2227 (class 0 OID 33098)
-- Dependencies: 193
-- Data for Name: reputation; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO reputation (id, category, points, created) VALUES (1, 'upvoted_question', 5, '2017-06-08 03:03:02');
INSERT INTO reputation (id, category, points, created) VALUES (2, 'upvoted_answer', 10, '2017-06-08 03:03:02');
INSERT INTO reputation (id, category, points, created) VALUES (3, 'accepted_answer', 15, '2017-06-08 03:03:02');
INSERT INTO reputation (id, category, points, created) VALUES (4, 'downvoted_question', -2, '2017-06-08 03:03:02');
INSERT INTO reputation (id, category, points, created) VALUES (5, 'downvoted_answer', -2, '2017-06-08 03:03:02');


--
-- TOC entry 2244 (class 0 OID 0)
-- Dependencies: 192
-- Name: reputation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('reputation_id_seq', 5, true);


--
-- TOC entry 2223 (class 0 OID 24645)
-- Dependencies: 189
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO tag (id, name) VALUES (1, 'python');
INSERT INTO tag (id, name) VALUES (2, 'sql');
INSERT INTO tag (id, name) VALUES (3, 'css');


--
-- TOC entry 2245 (class 0 OID 0)
-- Dependencies: 188
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('tag_id_seq', 3, true);


--
-- TOC entry 2225 (class 0 OID 33066)
-- Dependencies: 191
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO users (id, user_name, reputation, reg_time) VALUES (3, 'Mangal Ica', 0, '2017-06-07 20:34:14');
INSERT INTO users (id, user_name, reputation, reg_time) VALUES (1, 'Teszt Elek', 3, '2017-06-07 11:27:14');
INSERT INTO users (id, user_name, reputation, reg_time) VALUES (2, 'Beka Kálmán', 15, '2017-06-07 20:33:23');


--
-- TOC entry 2246 (class 0 OID 0)
-- Dependencies: 190
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('users_id_seq', 3, true);


--
-- TOC entry 2078 (class 2606 OID 24653)
-- Name: pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- TOC entry 2080 (class 2606 OID 24655)
-- Name: pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- TOC entry 2076 (class 2606 OID 24657)
-- Name: pk_question_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- TOC entry 2082 (class 2606 OID 24659)
-- Name: pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- TOC entry 2084 (class 2606 OID 24661)
-- Name: pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- TOC entry 2090 (class 2606 OID 33106)
-- Name: reputation_category_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY reputation
    ADD CONSTRAINT reputation_category_key UNIQUE (category);


--
-- TOC entry 2092 (class 2606 OID 33104)
-- Name: reputation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY reputation
    ADD CONSTRAINT reputation_pkey PRIMARY KEY (id);


--
-- TOC entry 2086 (class 2606 OID 33095)
-- Name: unique_user; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY users
    ADD CONSTRAINT unique_user UNIQUE (user_name);


--
-- TOC entry 2088 (class 2606 OID 33073)
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 2096 (class 2606 OID 33084)
-- Name: fk_accepted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_accepted_by FOREIGN KEY (accepted_by) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2097 (class 2606 OID 24662)
-- Name: fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2095 (class 2606 OID 33079)
-- Name: fk_answered_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_answered_by FOREIGN KEY (answered_by) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2094 (class 2606 OID 24667)
-- Name: fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2099 (class 2606 OID 24672)
-- Name: fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2098 (class 2606 OID 24677)
-- Name: fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2100 (class 2606 OID 24682)
-- Name: fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2093 (class 2606 OID 33074)
-- Name: fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2017-06-08 10:44:21 CEST

--
-- PostgreSQL database dump complete
--

