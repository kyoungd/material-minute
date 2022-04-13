--
-- PostgreSQL database dump
--

-- Dumped from database version 12.10 (Ubuntu 12.10-1.pgdg20.04+1+b1)
-- Dumped by pg_dump version 14.2 (Ubuntu 14.2-1.pgdg20.04+1+b1)

-- Started on 2022-04-12 17:34:34 PDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 202 (class 1259 OID 38836)
-- Name: _prisma_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public._prisma_migrations (
    id character varying(36) NOT NULL,
    checksum character varying(64) NOT NULL,
    finished_at timestamp with time zone,
    migration_name character varying(255) NOT NULL,
    logs text,
    rolled_back_at timestamp with time zone,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    applied_steps_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public._prisma_migrations OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 222037)
-- Name: asset; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.asset (
    id bigint NOT NULL,
    symbol character varying(16),
    timeframe character varying(8),
    datetime_at timestamp with time zone,
    high numeric,
    low numeric,
    open numeric,
    close numeric,
    volume numeric
);


ALTER TABLE public.asset OWNER TO admin;

--
-- TOC entry 216 (class 1259 OID 222040)
-- Name: asset_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.asset ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.asset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 211 (class 1259 OID 38974)
-- Name: company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company (
    name character varying(255) NOT NULL,
    search_term character varying(511) DEFAULT ''::character varying NOT NULL,
    "createdAt" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    class character varying(15) NOT NULL,
    easy_to_borrow boolean NOT NULL,
    exchange character varying(15) NOT NULL,
    fractionable boolean NOT NULL,
    id character varying(39) NOT NULL,
    shortable boolean NOT NULL,
    status character varying(15) NOT NULL,
    symbol character varying(15) NOT NULL,
    tradable boolean NOT NULL,
    review_search boolean DEFAULT false NOT NULL,
    marginable boolean NOT NULL
);


ALTER TABLE public.company OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 324444)
-- Name: market_attribute; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.market_attribute (
    symbol character varying(16) NOT NULL,
    volume_profile_coc json
);


ALTER TABLE public.market_attribute OWNER TO admin;

--
-- TOC entry 214 (class 1259 OID 55291)
-- Name: market_data; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.market_data (
    id integer NOT NULL,
    symbol character varying(16) NOT NULL,
    data json,
    datatype character varying(8) NOT NULL,
    timeframe character varying(8) NOT NULL,
    name character varying(256) NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    is_deleted boolean DEFAULT false,
    atr45 numeric,
    atr90 numeric,
    atr180 numeric,
    close numeric,
    volume bigint,
    volatility01 numeric,
    volatility03 numeric,
    volatility30 numeric,
    keylevels json,
    is_first_key_level_min boolean,
    attribute json
);


ALTER TABLE public.market_data OWNER TO admin;

--
-- TOC entry 3076 (class 0 OID 0)
-- Dependencies: 214
-- Name: COLUMN market_data.attribute; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.market_data.attribute IS 'attributes of the stock.  General data.';


--
-- TOC entry 213 (class 1259 OID 55289)
-- Name: market_data_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.market_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.market_data_id_seq OWNER TO admin;

--
-- TOC entry 3077 (class 0 OID 0)
-- Dependencies: 213
-- Name: market_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.market_data_id_seq OWNED BY public.market_data.id;


--
-- TOC entry 217 (class 1259 OID 304638)
-- Name: news; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.news (
    id bigint NOT NULL,
    headline character varying(1024),
    author character varying(64),
    summary text,
    url character varying(512),
    news_at timestamp with time zone,
    sentiment numeric
);


ALTER TABLE public.news OWNER TO admin;

--
-- TOC entry 210 (class 1259 OID 38960)
-- Name: news_symbol; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news_symbol (
    id integer NOT NULL,
    symbol character varying(15) NOT NULL,
    pub_date timestamp(3) without time zone NOT NULL,
    "createdAt" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_update timestamp(3) without time zone NOT NULL,
    active_until timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.news_symbol OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 38958)
-- Name: news_symbol_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.news_symbol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.news_symbol_id_seq OWNER TO postgres;

--
-- TOC entry 3078 (class 0 OID 0)
-- Dependencies: 209
-- Name: news_symbol_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.news_symbol_id_seq OWNED BY public.news_symbol.id;


--
-- TOC entry 218 (class 1259 OID 304646)
-- Name: news_symbols; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.news_symbols (
    id bigint,
    symbol character(16)[]
);


ALTER TABLE public.news_symbols OWNER TO admin;

--
-- TOC entry 206 (class 1259 OID 38860)
-- Name: site_google; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.site_google (
    id integer NOT NULL,
    symbol character varying(15) NOT NULL,
    title character varying(511) NOT NULL,
    description text NOT NULL,
    pub_date timestamp(3) without time zone NOT NULL,
    link character varying(1023) NOT NULL,
    sentiment double precision DEFAULT 0 NOT NULL,
    "createdAt" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.site_google OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 38858)
-- Name: site_google_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.site_google_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.site_google_id_seq OWNER TO postgres;

--
-- TOC entry 3079 (class 0 OID 0)
-- Dependencies: 205
-- Name: site_google_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.site_google_id_seq OWNED BY public.site_google.id;


--
-- TOC entry 212 (class 1259 OID 47108)
-- Name: site_sec; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.site_sec (
    symbol character varying(16) NOT NULL,
    cik character varying(16) NOT NULL,
    market_close double precision,
    market_close_at date,
    float_percent numeric,
    float_volume bigint,
    float_at date
);


ALTER TABLE public.site_sec OWNER TO admin;

--
-- TOC entry 208 (class 1259 OID 38938)
-- Name: site_twitter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.site_twitter (
    id integer NOT NULL,
    symbol character varying(15) NOT NULL,
    description text NOT NULL,
    pub_date timestamp(3) without time zone NOT NULL,
    sentiment double precision DEFAULT 0 NOT NULL,
    "createdAt" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    link character varying(1023) NOT NULL,
    title character varying(511) NOT NULL
);


ALTER TABLE public.site_twitter OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 38936)
-- Name: site_twitter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.site_twitter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.site_twitter_id_seq OWNER TO postgres;

--
-- TOC entry 3080 (class 0 OID 0)
-- Dependencies: 207
-- Name: site_twitter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.site_twitter_id_seq OWNED BY public.site_twitter.id;


--
-- TOC entry 204 (class 1259 OID 38848)
-- Name: site_yahoo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.site_yahoo (
    id integer NOT NULL,
    symbol character varying(15) NOT NULL,
    title character varying(511) NOT NULL,
    description text NOT NULL,
    pub_date timestamp(3) without time zone NOT NULL,
    link character varying(1023) NOT NULL,
    sentiment double precision DEFAULT 0 NOT NULL,
    "createdAt" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.site_yahoo OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 38846)
-- Name: site_yahoo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.site_yahoo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.site_yahoo_id_seq OWNER TO postgres;

--
-- TOC entry 3081 (class 0 OID 0)
-- Dependencies: 203
-- Name: site_yahoo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.site_yahoo_id_seq OWNED BY public.site_yahoo.id;


--
-- TOC entry 2913 (class 2604 OID 55294)
-- Name: market_data id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.market_data ALTER COLUMN id SET DEFAULT nextval('public.market_data_id_seq'::regclass);


--
-- TOC entry 2906 (class 2604 OID 38963)
-- Name: news_symbol id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_symbol ALTER COLUMN id SET DEFAULT nextval('public.news_symbol_id_seq'::regclass);


--
-- TOC entry 2900 (class 2604 OID 38863)
-- Name: site_google id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_google ALTER COLUMN id SET DEFAULT nextval('public.site_google_id_seq'::regclass);


--
-- TOC entry 2903 (class 2604 OID 38941)
-- Name: site_twitter id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_twitter ALTER COLUMN id SET DEFAULT nextval('public.site_twitter_id_seq'::regclass);


--
-- TOC entry 2897 (class 2604 OID 38851)
-- Name: site_yahoo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_yahoo ALTER COLUMN id SET DEFAULT nextval('public.site_yahoo_id_seq'::regclass);


--
-- TOC entry 2916 (class 2606 OID 38845)
-- Name: _prisma_migrations _prisma_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public._prisma_migrations
    ADD CONSTRAINT _prisma_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 2931 (class 2606 OID 38990)
-- Name: company company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_pkey PRIMARY KEY (symbol);


--
-- TOC entry 2936 (class 2606 OID 55299)
-- Name: market_data market_data_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.market_data
    ADD CONSTRAINT market_data_pkey PRIMARY KEY (id);


--
-- TOC entry 2940 (class 2606 OID 304645)
-- Name: news news_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_pkey PRIMARY KEY (id);


--
-- TOC entry 2927 (class 2606 OID 38966)
-- Name: news_symbol news_symbol_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_symbol
    ADD CONSTRAINT news_symbol_pkey PRIMARY KEY (id);


--
-- TOC entry 2922 (class 2606 OID 38869)
-- Name: site_google site_google_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_google
    ADD CONSTRAINT site_google_pkey PRIMARY KEY (id);


--
-- TOC entry 2925 (class 2606 OID 38947)
-- Name: site_twitter site_twitter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_twitter
    ADD CONSTRAINT site_twitter_pkey PRIMARY KEY (id);


--
-- TOC entry 2919 (class 2606 OID 38857)
-- Name: site_yahoo site_yahoo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_yahoo
    ADD CONSTRAINT site_yahoo_pkey PRIMARY KEY (id);


--
-- TOC entry 2929 (class 1259 OID 38998)
-- Name: company_id_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX company_id_key ON public.company USING btree (id);


--
-- TOC entry 2932 (class 1259 OID 38999)
-- Name: company_symbol_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX company_symbol_key ON public.company USING btree (symbol);


--
-- TOC entry 2934 (class 1259 OID 73745)
-- Name: datatype_ix; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX datatype_ix ON public.market_data USING btree (datatype, timeframe, symbol);


--
-- TOC entry 2933 (class 1259 OID 47111)
-- Name: ix_symbol; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_symbol ON public.site_sec USING btree (symbol);

ALTER TABLE public.site_sec CLUSTER ON ix_symbol;


--
-- TOC entry 2938 (class 1259 OID 222048)
-- Name: ix_symbol_timeframe_datetime_at; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_symbol_timeframe_datetime_at ON public.asset USING btree (symbol, timeframe, datetime_at DESC NULLS LAST);


--
-- TOC entry 2928 (class 1259 OID 38967)
-- Name: news_symbol_symbol_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX news_symbol_symbol_key ON public.news_symbol USING btree (symbol);


--
-- TOC entry 2920 (class 1259 OID 38971)
-- Name: site_google_link_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX site_google_link_key ON public.site_google USING btree (link);


--
-- TOC entry 2923 (class 1259 OID 38972)
-- Name: site_twitter_link_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX site_twitter_link_key ON public.site_twitter USING btree (link);


--
-- TOC entry 2917 (class 1259 OID 38973)
-- Name: site_yahoo_link_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX site_yahoo_link_key ON public.site_yahoo USING btree (link);


--
-- TOC entry 2937 (class 1259 OID 55301)
-- Name: symbols_combo_ix; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX symbols_combo_ix ON public.market_data USING btree (symbol, datatype, timeframe);

ALTER TABLE public.market_data CLUSTER ON symbols_combo_ix;


--
-- TOC entry 2944 (class 2606 OID 39000)
-- Name: news_symbol news_symbol_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_symbol
    ADD CONSTRAINT news_symbol_symbol_fkey FOREIGN KEY (symbol) REFERENCES public.company(symbol) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 2942 (class 2606 OID 39997)
-- Name: site_google site_google_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_google
    ADD CONSTRAINT site_google_symbol_fkey FOREIGN KEY (symbol) REFERENCES public.news_symbol(symbol) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 2943 (class 2606 OID 40002)
-- Name: site_twitter site_twitter_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_twitter
    ADD CONSTRAINT site_twitter_symbol_fkey FOREIGN KEY (symbol) REFERENCES public.news_symbol(symbol) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 2941 (class 2606 OID 39992)
-- Name: site_yahoo site_yahoo_symbol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_yahoo
    ADD CONSTRAINT site_yahoo_symbol_fkey FOREIGN KEY (symbol) REFERENCES public.news_symbol(symbol) ON UPDATE CASCADE ON DELETE RESTRICT;


-- Completed on 2022-04-12 17:34:34 PDT

--
-- PostgreSQL database dump complete
--

