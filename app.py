import streamlit as st
import pandas as pd
import joblib
import base64
import os
import sqlite3
from datetime import datetime

from sklearn.pipeline import Pipeline


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CropCompass",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

@property --angle {
    syntax: '<angle>';
    initial-value: 0deg;
    inherits: false;
}

:root {
    --green-950: #081c13;
    --green-900: #0d2a1c;
    --green-800: #14402b;
    --green-700: #1a5538;
    --green-600: #1f6b43;
    --green-500: #2f8a5a;
    --green-100: #e3f1e8;
    --green-50: #f1f8f3;

    --gold: #c9a24b;

    --ink: #13241a;
    --muted: #5f6d64;
    --line: #e1e8e3;
    --canvas: #f4f6f4;
    --white: #ffffff;

    --ease: cubic-bezier(.22, 1, .36, 1);
}


/* =========================================================
   GLOBAL
========================================================= */

html,
body,
[class*="css"],
.stApp,
button,
input,
select,
textarea {

    font-family:
        'Inter',
        -apple-system,
        'Segoe UI',
        Roboto,
        sans-serif;

    font-feature-settings:
        'tnum' 1,
        'cv11' 1;
}


.stApp {

    background:
        radial-gradient(
            900px 500px at 100% -10%,
            rgba(47,138,90,.08),
            transparent 60%
        ),
        var(--canvas);
}


.block-container {

    max-width: 1450px;

    padding-top: 2.2rem;
    padding-bottom: 4rem;

    padding-left: 3rem;
    padding-right: 3rem;
}


#MainMenu,
footer,
[data-testid="stToolbar"],
[data-testid="stDeployButton"] {

    visibility: hidden;
}


header[data-testid="stHeader"] {
    background: transparent;
}


h1,
h2,
h3 {

    color: var(--ink);
    letter-spacing: -0.02em;
}


/* =========================================================
   PAGE ENTRANCE
========================================================= */

@keyframes fadeUp {

    from {
        opacity: 0;
        transform: translateY(18px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}


.block-container [data-testid="stElementContainer"] {

    animation:
        fadeUp .7s var(--ease) both;
}


.block-container [data-testid="stElementContainer"]:nth-child(1) {
    animation-delay: .00s;
}

.block-container [data-testid="stElementContainer"]:nth-child(2) {
    animation-delay: .07s;
}

.block-container [data-testid="stElementContainer"]:nth-child(3) {
    animation-delay: .14s;
}

.block-container [data-testid="stElementContainer"]:nth-child(4) {
    animation-delay: .21s;
}

.block-container [data-testid="stElementContainer"]:nth-child(5) {
    animation-delay: .28s;
}

.block-container [data-testid="stElementContainer"]:nth-child(6) {
    animation-delay: .35s;
}

.block-container [data-testid="stElementContainer"]:nth-child(n+7) {
    animation-delay: .42s;
}


/* =========================================================
   SIDEBAR
========================================================= */

[data-testid="stSidebar"] {

    background:
        radial-gradient(
            400px 300px at 0% 0%,
            rgba(47,138,90,.25),
            transparent 70%
        ),
        linear-gradient(
            180deg,
            var(--green-900),
            var(--green-950)
        );

    border-right:
        1px solid rgba(255,255,255,.04);
}


[data-testid="stSidebar"] > div:first-child {

    padding-top: 1.5rem;
    padding-left: .65rem;
    padding-right: .65rem;
}


[data-testid="stSidebar"] * {
    color: #ffffff;
}


/* =========================================================
   SIDEBAR BRAND
========================================================= */

.sidebar-brand {

    padding:
        8px
        10px
        24px
        10px;

    margin-bottom: 22px;

    border-bottom:
        1px solid rgba(255,255,255,.10);
}


.sidebar-title {

    font-size: 29px;
    font-weight: 800;

    letter-spacing: -1.2px;

    line-height: 1.1;

    background:
        linear-gradient(
            100deg,
            #ffffff,
            #a9e4c2,
            #ffffff
        );

    background-size: 220% 100%;

    -webkit-background-clip: text;
    background-clip: text;

    -webkit-text-fill-color: transparent;

    animation:
        brandShine 7s ease-in-out infinite;
}


@keyframes brandShine {

    0%,
    100% {
        background-position: 100% 0;
    }

    50% {
        background-position: 0 0;
    }

}


.sidebar-subtitle {

    font-size: 12.5px;

    color: #a9c7b5 !important;

    margin-top: 8px;

    line-height: 1.5;

    max-width: 210px;
}


.sidebar-section {

    font-size: 10.5px;

    font-weight: 700;

    letter-spacing: 1.5px;

    text-transform: uppercase;

    color: #7fa28d !important;

    padding:
        0
        10px;

    margin-bottom: 9px;
}


/* =========================================================
   SIDEBAR NAVIGATION
========================================================= */

[data-testid="stSidebar"]
div[role="radiogroup"] {

    gap: 4px;
}


[data-testid="stSidebar"]
div[role="radiogroup"] > label {

    width: 100%;

    padding:
        11px
        14px;

    border-radius: 11px;

    margin: 0;

    cursor: pointer;

    position: relative;

    transition:
        background-color .25s var(--ease),
        transform .25s var(--ease);
}


[data-testid="stSidebar"]
div[role="radiogroup"]
> label > div:first-child {

    display: none;
}


[data-testid="stSidebar"]
div[role="radiogroup"]
> label p {

    font-size: 14.5px;

    font-weight: 500;

    color: #bcd5c5 !important;

    transition:
        color .25s ease;
}


[data-testid="stSidebar"]
div[role="radiogroup"]
> label:hover {

    background-color:
        rgba(255,255,255,.07);

    transform:
        translateX(4px);
}


[data-testid="stSidebar"]
div[role="radiogroup"]
> label:has(input:checked) {

    background:
        linear-gradient(
            90deg,
            rgba(255,255,255,.16),
            rgba(255,255,255,.05)
        );

    box-shadow:
        0 8px 20px rgba(0,0,0,.10);
}


[data-testid="stSidebar"]
div[role="radiogroup"]
> label:has(input:checked)::before {

    content: "";

    position: absolute;

    left: 0;

    top: 18%;
    bottom: 18%;

    width: 3px;

    border-radius: 3px;

    background:
        var(--gold);

    animation:
        barIn .35s var(--ease) both;
}


@keyframes barIn {

    from {
        transform: scaleY(0);
    }

    to {
        transform: scaleY(1);
    }

}


[data-testid="stSidebar"]
div[role="radiogroup"]
> label:has(input:checked) p {

    color: #ffffff !important;

    font-weight: 700;
}


/* =========================================================
   PAGE HEADER
========================================================= */

.page-title {

    color: var(--ink);

    font-size: 37px;

    font-weight: 800;

    letter-spacing: -1.2px;

    line-height: 1.15;
}


.page-description {

    color: var(--muted);

    font-size: 15.5px;

    line-height: 1.65;

    margin-top: 9px;

    max-width: 760px;
}


.page-divider {

    height: 2px;

    width: 100%;

    margin:
        26px
        0
        30px
        0;

    background:
        linear-gradient(
            90deg,
            var(--green-600) 0 72px,
            var(--line) 72px 100%
        );

    transform-origin: left;

    animation:
        lineGrow .9s var(--ease) both;
}


@keyframes lineGrow {

    from {
        transform: scaleX(.05);
        opacity: 0;
    }

    to {
        transform: scaleX(1);
        opacity: 1;
    }

}


/* =========================================================
   HERO
========================================================= */

.hero {

    position: relative;

    overflow: hidden;

    isolation: isolate;

    background:
        linear-gradient(
            135deg,
            #0a2819 0%,
            #17583a 100%
        );

    border-radius: 24px;

    padding:
        72px
        64px;

    margin-bottom: 34px;

    color: white;

    box-shadow:
        0 24px 60px -24px
        rgba(8,28,19,.55);

    min-height: 470px;

    display: flex;

    flex-direction: column;

    justify-content: center;
}


.hero::before {

    content: "";

    position: absolute;

    inset: -40%;

    z-index: -2;

    background:

        radial-gradient(
            35% 35% at 25% 30%,
            rgba(79,190,130,.35),
            transparent 70%
        ),

        radial-gradient(
            30% 30% at 75% 65%,
            rgba(201,162,75,.20),
            transparent 70%
        );

    animation:
        aurora 16s ease-in-out infinite alternate;
}


.hero::after {

    content: "";

    position: absolute;

    inset: 0;

    z-index: -1;

    background-image:

        linear-gradient(
            rgba(255,255,255,.05) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,255,255,.05) 1px,
            transparent 1px
        );

    background-size:
        44px 44px;

    -webkit-mask-image:
        radial-gradient(
            70% 90% at 80% 20%,
            #000,
            transparent 75%
        );

    mask-image:
        radial-gradient(
            70% 90% at 80% 20%,
            #000,
            transparent 75%
        );

    animation:
        gridPan 30s linear infinite;
}


@keyframes aurora {

    from {
        transform:
            translate3d(-4%, -3%, 0)
            rotate(0deg);
    }

    to {
        transform:
            translate3d(5%, 4%, 0)
            rotate(8deg);
    }

}


@keyframes gridPan {

    to {
        background-position:
            44px 44px,
            44px 44px;
    }

}


.hero-label {

    font-size: 12px;

    font-weight: 600;

    letter-spacing: 1.6px;

    text-transform: uppercase;

    color: #a9d3b9;

    margin-bottom: 16px;
}


.hero-title {

    font-size: 56px;

    font-weight: 800;

    line-height: 1.06;

    letter-spacing: -2.2px;

    margin: 0;

    background:
        linear-gradient(
            100deg,
            #ffffff 30%,
            #bfe8cf 50%,
            #ffffff 70%
        );

    background-size:
        220% 100%;

    -webkit-background-clip: text;

    background-clip: text;

    -webkit-text-fill-color: transparent;

    animation:
        sheen 7s ease-in-out infinite;
}


@keyframes sheen {

    0%,
    100% {
        background-position: 100% 0;
    }

    50% {
        background-position: 0 0;
    }

}


.hero-description {

    max-width: 720px;

    margin-top: 22px;

    font-size: 17px;

    line-height: 1.75;

    color: #d3e7da;
}


.hero-status {

    display: inline-flex;

    align-items: center;

    gap: 10px;

    margin-top: 28px;

    padding:
        9px
        17px;

    border-radius: 999px;

    background:
        rgba(255,255,255,.08);

    border:
        1px solid
        rgba(255,255,255,.16);

    backdrop-filter:
        blur(6px);

    font-size: 12.5px;

    font-weight: 500;

    align-self: flex-start;
}


.hero-status::before {

    content: "";

    width: 8px;
    height: 8px;

    border-radius: 50%;

    background:
        #5ee0a0;

    animation:
        pulse 2s ease-out infinite;
}


@keyframes pulse {

    0% {
        box-shadow:
            0 0 0 0
            rgba(94,224,160,.65);
    }

    100% {
        box-shadow:
            0 0 0 12px
            rgba(94,224,160,0);
    }

}


/* =========================================================
   SECTION HEADINGS
========================================================= */

.section-title {

    color: var(--ink);

    font-size: 23px;

    font-weight: 750;

    letter-spacing: -0.5px;

    margin-top: 8px;

    margin-bottom: 5px;
}


.section-subtitle {

    color: var(--muted);

    font-size: 14.5px;

    margin-bottom: 20px;
}


/* =========================================================
   METRIC CARDS
========================================================= */

[data-testid="stMetric"] {

    position: relative;

    overflow: hidden;

    background:
        var(--white);

    border:
        1px solid
        var(--line);

    border-radius: 17px;

    padding:
        23px
        24px;

    min-height: 125px;

    transition:
        transform .4s var(--ease),
        box-shadow .4s var(--ease),
        border-color .3s ease;
}


[data-testid="stMetric"]::before {

    content: "";

    position: absolute;

    left: 0;
    top: 0;

    height: 3px;

    width: 100%;

    background:
        linear-gradient(
            90deg,
            var(--green-500),
            var(--gold)
        );

    transform:
        scaleX(0);

    transform-origin: left;

    transition:
        transform .5s var(--ease);
}


[data-testid="stMetric"]:hover {

    transform:
        translateY(-5px);

    border-color:
        #c8d9ce;

    box-shadow:
        0 18px 40px -18px
        rgba(20,64,43,.28);
}


[data-testid="stMetric"]:hover::before {

    transform:
        scaleX(1);
}


[data-testid="stMetricLabel"] p {

    color:
        var(--muted) !important;

    font-size:
        13.5px;

    font-weight:
        500;
}


[data-testid="stMetricValue"] {

    color:
        var(--green-800) !important;

    font-weight:
        800;

    letter-spacing:
        -1px;
}


/* =========================================================
   MODEL CARDS
========================================================= */

.model-card {

    position: relative;

    overflow: hidden;

    background:
        var(--white);

    border:
        1px solid
        var(--line);

    border-radius:
        17px;

    padding:
        30px;

    min-height:
        175px;

    transition:
        transform .4s var(--ease),
        box-shadow .4s var(--ease),
        border-color .3s ease;
}


.model-card:hover {

    transform:
        translateY(-5px);

    border-color:
        #c8d9ce;

    box-shadow:
        0 18px 40px -18px
        rgba(20,64,43,.28);
}


.model-card-selected {

    border:
        1.5px solid transparent;

    background:
        linear-gradient(
            var(--green-50),
            var(--green-50)
        ) padding-box,

        conic-gradient(
            from var(--angle),
            #2f8a5a,
            #c9a24b,
            #2f8a5a,
            #7fd1a2,
            #2f8a5a
        ) border-box;

    animation:
        spin 6s linear infinite;
}


@keyframes spin {

    to {
        --angle: 360deg;
    }

}


.model-name {

    color:
        var(--ink);

    font-size:
        17px;

    font-weight:
        600;
}


.model-accuracy {

    color:
        var(--green-600);

    font-size:
        43px;

    font-weight:
        800;

    letter-spacing:
        -1.7px;

    margin-top:
        10px;

    line-height:
        1.1;
}


.model-caption {

    color:
        var(--muted);

    font-size:
        13px;

    margin-top:
        5px;
}


.model-badge {

    display:
        inline-block;

    margin-top:
        14px;

    padding:
        5px 12px;

    border-radius:
        999px;

    background:
        var(--green-100);

    color:
        var(--green-700);

    font-size:
        12px;

    font-weight:
        600;
}


/* =========================================================
   PROCESS CARDS
========================================================= */

.process-card {

    position: relative;

    overflow: hidden;

    background:
        var(--white);

    border:
        1px solid
        var(--line);

    border-radius:
        16px;

    padding:
        30px;

    min-height:
        195px;

    transition:
        transform .4s var(--ease),
        box-shadow .4s var(--ease),
        border-color .3s ease;
}


.process-card:hover {

    transform:
        translateY(-5px);

    border-color:
        #c8d9ce;

    box-shadow:
        0 18px 40px -18px
        rgba(20,64,43,.28);
}


.process-number {

    display:
        inline-flex;

    align-items:
        center;

    justify-content:
        center;

    width:
        36px;

    height:
        36px;

    border-radius:
        10px;

    background:
        linear-gradient(
            135deg,
            var(--green-700),
            var(--green-500)
        );

    color:
        #fff;

    font-size:
        13px;

    font-weight:
        700;

    margin-bottom:
        16px;
}


.process-title {

    color:
        var(--ink);

    font-size:
        18px;

    font-weight:
        700;

    margin-bottom:
        8px;
}


.process-text {

    color:
        var(--muted);

    font-size:
        14.5px;

    line-height:
        1.65;
}


/* =========================================================
   INPUT PANELS
========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background:
        var(--white);

    border-color:
        var(--line);

    border-radius:
        16px;

    transition:
        box-shadow .4s var(--ease),
        border-color .3s ease;
}


div[data-testid="stVerticalBlockBorderWrapper"]:hover {

    border-color:
        #c8d9ce;

    box-shadow:
        0 14px 34px -20px
        rgba(20,64,43,.3);
}


.input-group-title {

    color:
        var(--ink);

    font-size:
        12px;

    font-weight:
        700;

    letter-spacing:
        1px;

    text-transform:
        uppercase;

    margin-bottom:
        6px;
}


.info-note {

    background:
        var(--green-50);

    border:
        1px solid
        var(--line);

    border-radius:
        12px;

    padding:
        14px 16px;

    margin-top:
        14px;

    color:
        var(--muted);

    font-size:
        13px;

    line-height:
        1.6;
}


.info-note b {
    color:
        var(--green-800);
}


[data-testid="stWidgetLabel"] p {

    color:
        #33473a;

    font-size:
        13.5px;

    font-weight:
        500;
}


div[data-baseweb="input"],
div[data-baseweb="select"] {

    border-radius:
        10px;

    transition:
        box-shadow .25s ease,
        border-color .25s ease;
}


div[data-baseweb="input"]:focus-within {

    border-color:
        var(--green-500) !important;

    box-shadow:
        0 0 0 4px
        rgba(47,138,90,.14);
}


/* =========================================================
   RESULT BOX
========================================================= */

.result-box {

    position:
        relative;

    overflow:
        hidden;

    background:
        linear-gradient(
            135deg,
            #0d2a1c,
            #1a5538
        );

    border-radius:
        18px;

    padding:
        40px 24px;

    text-align:
        center;

    box-shadow:
        0 22px 50px -22px
        rgba(8,28,19,.6);

    animation:
        popIn .8s var(--ease) both;
}


.result-label {

    color:
        #a9d3b9;

    font-size:
        12px;

    font-weight:
        600;

    letter-spacing:
        1.6px;

    text-transform:
        uppercase;
}


.result-crop {

    color:
        #ffffff;

    font-size:
        48px;

    font-weight:
        800;

    letter-spacing:
        -1.4px;

    margin-top:
        8px;
}


@keyframes popIn {

    from {

        opacity:
            0;

        transform:
            scale(.96)
            translateY(10px);
    }

    to {

        opacity:
            1;

        transform:
            scale(1)
            translateY(0);
    }

}


/* =========================================================
   TOP 3 CARDS
========================================================= */

.rank-card {

    background:
        var(--white);

    border:
        1px solid
        var(--line);

    border-radius:
        16px;

    padding:
        20px 22px;

    transition:
        transform .4s var(--ease),
        box-shadow .4s var(--ease);
}


.rank-card:hover {

    transform:
        translateY(-5px);

    box-shadow:
        0 18px 40px -18px
        rgba(20,64,43,.28);
}


.rank-top {

    display:
        flex;

    justify-content:
        space-between;

    align-items:
        baseline;
}


.rank-pos {

    color:
        var(--muted);

    font-size:
        12px;

    font-weight:
        700;

    letter-spacing:
        1px;
}


.rank-score {

    color:
        var(--green-700);

    font-size:
        26px;

    font-weight:
        800;

    letter-spacing:
        -.8px;
}


.rank-name {

    color:
        var(--ink);

    font-size:
        17px;

    font-weight:
        600;

    margin:
        6px 0 14px 0;
}


.rank-track {

    height:
        6px;

    background:
        var(--green-100);

    border-radius:
        99px;

    overflow:
        hidden;
}


.rank-fill {

    height:
        100%;

    border-radius:
        99px;

    background:
        linear-gradient(
            90deg,
            var(--green-600),
            #5ec28f
        );
}


.rank-1 .rank-fill {

    background:
        linear-gradient(
            90deg,
            var(--green-600),
            var(--gold)
        );
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button {

    position:
        relative;

    overflow:
        hidden;

    background:
        linear-gradient(
            135deg,
            var(--green-700),
            var(--green-500)
        );

    color:
        white;

    border:
        none;

    border-radius:
        12px;

    min-height:
        52px;

    font-size:
        15px;

    font-weight:
        600;

    letter-spacing:
        .2px;

    box-shadow:
        0 10px 24px -12px
        rgba(20,64,43,.7);

    transition:
        transform .3s var(--ease),
        box-shadow .3s var(--ease);
}


.stButton > button:hover {

    color:
        white;

    border:
        none;

    transform:
        translateY(-2px);

    box-shadow:
        0 16px 30px -12px
        rgba(20,64,43,.75);
}


.stButton > button:active {

    transform:
        translateY(0)
        scale(.99);
}


/* =========================================================
   ALERTS / TABLES
========================================================= */

[data-testid="stAlert"] {

    border-radius:
        12px;

    border:
        1px solid
        var(--line);
}


[data-testid="stDataFrame"] {

    border-radius:
        12px;

    overflow:
        hidden;
}


hr {

    border-color:
        var(--line);
}


[data-testid="stCaptionContainer"] {

    color:
        var(--muted);
}


/* =========================================================
   BACKGROUND PHOTO
========================================================= */

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {

    background:
        transparent;
}


/* =========================================================
   PIPELINE BAND
========================================================= */

.band {

    position:
        relative;

    overflow:
        hidden;

    border-radius:
        22px;

    padding:
        46px 44px 0 44px;

    margin-bottom:
        44px;

    color:
        #fff;

    background:
        linear-gradient(
            160deg,
            #0a1f15,
            #10382a
        );

    box-shadow:
        0 24px 60px -28px
        rgba(8,28,19,.6);
}


.band::before {

    content:
        "";

    position:
        absolute;

    inset:
        0;

    background:
        radial-gradient(
            520px 260px at 92% 0%,
            rgba(201,162,75,.18),
            transparent 70%
        );
}


.band-label {

    position:
        relative;

    font-size:
        12px;

    font-weight:
        600;

    letter-spacing:
        1.6px;

    text-transform:
        uppercase;

    color:
        var(--gold);
}


.band-title {

    position:
        relative;

    max-width:
        640px;

    margin:
        8px 0 32px 0;

    font-size:
        28px;

    font-weight:
        800;

    letter-spacing:
        -.8px;

    line-height:
        1.2;

    color:
        #fff;
}


.flow {

    position:
        relative;

    display:
        grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap:
        18px;
}


.flow-step {

    position:
        relative;

    padding:
        22px 20px;

    background:
        rgba(255,255,255,.06);

    border:
        1px solid
        rgba(255,255,255,.12);

    border-radius:
        16px;

    transition:
        transform .4s var(--ease),
        background .3s ease,
        border-color .3s ease;
}


.flow-step:hover {

    transform:
        translateY(-6px);

    background:
        rgba(255,255,255,.10);

    border-color:
        rgba(201,162,75,.65);
}


.flow-num {

    display:
        inline-flex;

    align-items:
        center;

    justify-content:
        center;

    width:
        38px;

    height:
        38px;

    margin-bottom:
        14px;

    border-radius:
        50%;

    background:
        #0f3a29;

    border:
        1px solid
        var(--gold);

    color:
        var(--gold);

    font-size:
        13px;

    font-weight:
        700;
}


.flow-step b {

    display:
        block;

    margin-bottom:
        6px;

    font-size:
        16px;

    color:
        #fff;
}


.flow-step p {

    margin:
        0;

    font-size:
        13.5px;

    line-height:
        1.6;

    color:
        #b9d3c3;
}


.ticker {

    margin:
        38px -44px 0 -44px;

    padding:
        18px 0;

    overflow:
        hidden;

    border-top:
        1px solid
        rgba(255,255,255,.10);
}


.ticker-track {

    display:
        flex;

    width:
        max-content;

    animation:
        marquee 45s linear infinite;
}


.tick {

    display:
        inline-flex;

    align-items:
        center;

    gap:
        16px;

    padding:
        0 18px;

    white-space:
        nowrap;

    font-size:
        13px;

    font-weight:
        600;

    letter-spacing:
        1.4px;

    text-transform:
        uppercase;

    color:
        #cfe5d7;
}


.tick::after {

    content:
        "";

    width:
        5px;

    height:
        5px;

    border-radius:
        50%;

    background:
        var(--gold);
}


@keyframes marquee {

    to {
        transform:
            translateX(-50%);
    }

}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 900px) {

    .block-container {

        padding-left:
            1.2rem;

        padding-right:
            1.2rem;
    }


    .hero {

        padding:
            42px 30px;

        min-height:
            400px;
    }


    .hero-title {

        font-size:
            40px;
    }


    .flow {

        grid-template-columns:
            1fr 1fr;
    }

}


@media (prefers-reduced-motion: reduce) {

    *,
    *::before,
    *::after {

        animation:
            none !important;

        transition:
            none !important;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# BACKGROUND IMAGE
# =========================================================

def load_hero_image():

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    for file_name, mime in [

        ("assets/hero_bg.jpg", "jpeg"),
        ("assets/hero_bg.jpeg", "jpeg"),
        ("assets/hero_bg.png", "png")

    ]:

        image_path = os.path.join(
            base_dir,
            file_name
        )

        if os.path.exists(image_path):

            with open(
                image_path,
                "rb"
            ) as image_file:

                image_data = base64.b64encode(
                    image_file.read()
                ).decode()

            return mime, image_data

    return None, None


hero_mime, hero_b64 = load_hero_image()


if hero_b64:

    st.markdown(
        f"""
<style>

:root {{
    --photo:
        url("data:image/{hero_mime};base64,{hero_b64}");
}}


/* HERO PHOTO */

.hero {{

    background:

        linear-gradient(
            90deg,
            rgba(6,24,16,.90) 0%,
            rgba(6,24,16,.62) 42%,
            rgba(6,24,16,.10) 100%
        ),

        var(--photo);

    background-position:
        center;

    background-size:
        cover;

    background-repeat:
        no-repeat;
}}


/* PAGE BACKGROUND */

.stApp {{

    background:

        linear-gradient(
            rgba(6,24,16,.34),
            rgba(6,24,16,.56)
        ),

        var(--photo);

    background-position:
        center;

    background-size:
        cover;

    background-repeat:
        no-repeat;

    background-attachment:
        fixed;
}}


/* CONTENT PANEL */

.block-container {{

    width:
        calc(100% - 3rem);

    margin:
        1.2rem auto;

    padding:
        2.5rem 2.5rem 4rem 2.5rem;

    background:
        rgba(244,246,244,.80);

    -webkit-backdrop-filter:
        blur(6px);

    backdrop-filter:
        blur(6px);

    border:
        1px solid
        rgba(255,255,255,.55);

    border-radius:
        26px;

    box-shadow:
        0 30px 80px -30px
        rgba(4,16,10,.65);
}}

</style>
""",
        unsafe_allow_html=True
    )

else:

    st.warning(
        "Background image not found. "
        "Check assets/hero_bg.jpg"
    )


# =========================================================
# HELPERS
# =========================================================

def page_header(title, description):

    st.markdown(
        f"""
<div class="page-title">{title}</div>

<div class="page-description">
{description}
</div>

<div class="page-divider"></div>
""",
        unsafe_allow_html=True
    )


def section_header(title, subtitle=None):

    st.markdown(
        f"""
<div class="section-title">
{title}
</div>
""",
        unsafe_allow_html=True
    )

    if subtitle:

        st.markdown(
            f"""
<div class="section-subtitle">
{subtitle}
</div>
""",
            unsafe_allow_html=True
        )


def spacer():

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


# =========================================================
# CROP LIST
# =========================================================

CROPS = [

    "Rice",
    "Maize",
    "Chickpea",
    "Kidney Beans",
    "Pigeon Peas",
    "Moth Beans",
    "Mung Bean",
    "Black Gram",
    "Lentil",
    "Pomegranate",
    "Banana",
    "Mango",
    "Grapes",
    "Watermelon",
    "Muskmelon",
    "Apple",
    "Orange",
    "Papaya",
    "Coconut",
    "Cotton",
    "Jute",
    "Coffee"

]


# =========================================================
# PIPELINE BAND
# =========================================================

def pipeline_band():

    ticker_items = "".join(

        f'<span class="tick">{crop}</span>'

        for crop in CROPS

    )

    st.markdown(
        f"""
<div class="band">

<div class="band-label">
Decision pipeline
</div>

<div class="band-title">
From field conditions to a confident crop decision
</div>

<div class="flow">

<div class="flow-step">

<div class="flow-num">01</div>

<b>Field inputs</b>

<p>
Nitrogen, phosphorus, potassium,
temperature, humidity, pH and rainfall.
</p>

</div>


<div class="flow-step">

<div class="flow-num">02</div>

<b>Preparation</b>

<p>
Feature names and scaling are matched
exactly to the training data.
</p>

</div>


<div class="flow-step">

<div class="flow-num">03</div>

<b>Model analysis</b>

<p>
Random Forest and Logistic Regression
evaluate the conditions.
</p>

</div>


<div class="flow-step">

<div class="flow-num">04</div>

<b>Recommendation</b>

<p>
A recommended crop with its top
alternatives and model score.
</p>

</div>

</div>


<div class="ticker">

<div class="ticker-track">

{ticker_items}
{ticker_items}

</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )


# =========================================================
# LOAD MODELS
# =========================================================

random_forest_model = joblib.load(
    "models/random_forest_model.pkl"
)


logistic_model = joblib.load(
    "models/logistic_model.pkl"
)


metadata = joblib.load(
    "models/cropcompass_metadata.pkl"
)


# =========================================================
# OPTIONAL SCALER
# =========================================================

try:

    scaler = joblib.load(
        "models/scaler.pkl"
    )

except FileNotFoundError:

    scaler = None


def prepare_input_for_logistic(data):

    if isinstance(
        logistic_model,
        Pipeline
    ):

        return data

    if scaler is not None:

        return pd.DataFrame(

            scaler.transform(data),

            columns=data.columns

        )

    return data


# =========================================================
# DATABASE
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)


DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "cropcompass.db"
)


def initialize_database():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            nitrogen REAL,
            phosphorus REAL,
            potassium REAL,

            temperature REAL,
            humidity REAL,

            ph REAL,
            rainfall REAL,

            random_forest_prediction TEXT,
            logistic_prediction TEXT,

            model_score REAL

        )
        """
    )

    connection.commit()

    connection.close()


initialize_database()


def save_prediction(
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    ph,
    rainfall,
    rf_prediction,
    lr_prediction,
    model_score
):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO prediction_history (

            timestamp,

            nitrogen,
            phosphorus,
            potassium,

            temperature,
            humidity,

            ph,
            rainfall,

            random_forest_prediction,
            logistic_prediction,

            model_score

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            nitrogen,
            phosphorus,
            potassium,

            temperature,
            humidity,

            ph,
            rainfall,

            rf_prediction,
            lr_prediction,

            model_score

        )
    )

    connection.commit()

    connection.close()


def load_prediction_history():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    history_df = pd.read_sql_query(
        """
        SELECT
            id,
            timestamp,
            nitrogen AS N,
            phosphorus AS P,
            potassium AS K,
            temperature,
            humidity,
            ph,
            rainfall,
            random_forest_prediction AS "Random Forest",
            logistic_prediction AS "Logistic Regression",
            model_score AS "RF Score"
        FROM prediction_history
        ORDER BY id DESC
        """,
        connection
    )

    connection.close()

    return history_df


# =========================================================
# LOAD DATASET FOR EDA
# =========================================================

def load_dataset():

    possible_paths = [

        os.path.join(
            BASE_DIR,
            "Crop_recommendation.csv"
        ),

        os.path.join(
            BASE_DIR,
            "data",
            "Crop_recommendation.csv"
        ),

        os.path.join(
            BASE_DIR,
            "dataset",
            "Crop_recommendation.csv"
        )

    ]

    for path in possible_paths:

        if os.path.exists(path):

            return pd.read_csv(path)

    return None


dataset = load_dataset()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
<div class="sidebar-brand">

<div class="sidebar-title">
🌱 CropCompass
</div>

<div class="sidebar-subtitle">
Data-driven crop decision support
</div>

</div>

<div class="sidebar-section">
Navigation
</div>
""",
    unsafe_allow_html=True
)


page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Dashboard",

        "🌾 Crop Prediction",

        "📊 Model Performance",

        "🔍 Explainability",

        "🧪 What-If Analysis",

        "📜 Prediction History",

        "📈 Dataset & EDA"

    ],

    label_visibility="collapsed"

)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
<div class="hero">

<div class="hero-label">
Machine Learning • Smart Agriculture
</div>

<div class="hero-title">
Smarter crop decisions,<br>
backed by data.
</div>

<div class="hero-description">

CropCompass analyzes soil and environmental
conditions using trained machine learning models
to provide data-driven crop recommendations.

</div>

<div class="hero-status">
Models ready for prediction
</div>

</div>
""",
        unsafe_allow_html=True
    )


    pipeline_band()


    section_header(

        "Project Overview",

        "A quick look at the dataset and machine learning system."

    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Dataset Records",
            "2,200"
        )


    with col2:

        st.metric(
            "Crop Classes",
            "22"
        )


    with col3:

        st.metric(
            "Input Features",
            "7"
        )


    with col4:

        st.metric(
            "Best Accuracy",
            "99.55%"
        )


    spacer()


    # -----------------------------------------------------
    # MODEL PERFORMANCE
    # -----------------------------------------------------

    section_header(

        "Model Performance",

        "Two classification algorithms were trained and compared."

    )


    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            """
<div class="model-card">

<div class="model-name">
Logistic Regression
</div>

<div class="model-accuracy">
97.27%
</div>

<div class="model-caption">
Test Accuracy
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
<div class="model-card model-card-selected">

<div class="model-name">
Random Forest
</div>

<div class="model-accuracy">
99.55%
</div>

<div class="model-caption">
Test Accuracy
</div>

<div class="model-badge">
✓ Selected model
</div>

</div>
""",
            unsafe_allow_html=True
        )


    spacer()


    # -----------------------------------------------------
    # HOW IT WORKS
    # -----------------------------------------------------

    section_header(

        "How CropCompass Works",

        "From input conditions to a machine learning prediction."

    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
<div class="process-card">

<div class="process-number">
1
</div>

<div class="process-title">
Enter Conditions
</div>

<div class="process-text">

Provide soil nutrient values and
environmental conditions such as
temperature, humidity, pH and rainfall.

</div>

</div>
""",
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
<div class="process-card">

<div class="process-number">
2
</div>

<div class="process-title">
Run Prediction
</div>

<div class="process-text">

The trained machine learning models
analyze the seven input features and
identify the most suitable crop category.

</div>

</div>
""",
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
<div class="process-card">

<div class="process-number">
3
</div>

<div class="process-title">
Understand Results
</div>

<div class="process-text">

View the recommended crop,
alternative predictions and agreement
between the trained models.

</div>

</div>
""",
            unsafe_allow_html=True
        )


    spacer()


    st.caption(

        "CropCompass is a decision-support system based on "
        "historical dataset patterns and should not be treated "
        "as a guaranteed agricultural recommendation."

    )


# =========================================================
# CROP PREDICTION
# =========================================================

elif page == "🌾 Crop Prediction":

    page_header(

        "Crop Prediction",

        "Enter the soil and environmental conditions to generate "
        "a crop prediction."

    )


    section_header(

        "Soil & Environmental Conditions",

        "Use values within the range represented in the training dataset."

    )


    col1, col2, col3 = st.columns(3)


    with col1:

        with st.container(border=True):

            st.markdown(
                '<div class="input-group-title">Soil Nutrients</div>',
                unsafe_allow_html=True
            )


            nitrogen = st.number_input(
                "Nitrogen (N)",
                min_value=0.0,
                max_value=140.0,
                value=50.0,
                step=0.1
            )


            phosphorus = st.number_input(
                "Phosphorus (P)",
                min_value=5.0,
                max_value=145.0,
                value=50.0,
                step=0.1
            )


            potassium = st.number_input(
                "Potassium (K)",
                min_value=5.0,
                max_value=205.0,
                value=50.0,
                step=0.1
            )


    with col2:

        with st.container(border=True):

            st.markdown(
                '<div class="input-group-title">Climate</div>',
                unsafe_allow_html=True
            )


            temperature = st.number_input(
                "Temperature (°C)",
                min_value=8.0,
                max_value=44.0,
                value=25.0,
                step=0.1
            )


            humidity = st.number_input(
                "Humidity (%)",
                min_value=14.0,
                max_value=100.0,
                value=70.0,
                step=0.1
            )


    with col3:

        with st.container(border=True):

            st.markdown(
                '<div class="input-group-title">Soil & Water</div>',
                unsafe_allow_html=True
            )


            ph = st.number_input(
                "Soil pH",
                min_value=3.5,
                max_value=9.9,
                value=6.5,
                step=0.1
            )


            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=20.0,
                max_value=299.0,
                value=100.0,
                step=0.1
            )


    spacer()


    if st.button(
        "🌱 Predict Crop",
        use_container_width=True
    ):


        input_data = pd.DataFrame(
            [{
                "N": nitrogen,
                "P": phosphorus,
                "K": potassium,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            }]
        )


        logistic_input = prepare_input_for_logistic(
            input_data
        )


        rf_prediction = random_forest_model.predict(
            input_data
        )[0]


        lr_prediction = logistic_model.predict(
            logistic_input
        )[0]


        rf_probabilities = random_forest_model.predict_proba(
            input_data
        )[0]


        class_names = random_forest_model.classes_


        sorted_indices = rf_probabilities.argsort()[::-1]


        top_3 = []


        for index in sorted_indices[:3]:

            top_3.append(

                (
                    class_names[index],
                    rf_probabilities[index] * 100
                )

            )


        predicted_index = list(
            class_names
        ).index(
            rf_prediction
        )


        model_score = (
            rf_probabilities[predicted_index]
            * 100
        )


        # SAVE TO DATABASE

        save_prediction(

            nitrogen,
            phosphorus,
            potassium,

            temperature,
            humidity,

            ph,
            rainfall,

            rf_prediction,
            lr_prediction,

            model_score

        )


        st.divider()


        section_header(
            "Prediction Result"
        )


        st.markdown(
            f"""
<div class="result-box">

<div class="result-label">
Recommended Crop
</div>

<div class="result-crop">
{rf_prediction.title()}
</div>

</div>
""",
            unsafe_allow_html=True
        )


        spacer()


        # -------------------------------------------------
        # TOP 3
        # -------------------------------------------------

        section_header(
            "Top 3 Recommendations"
        )


        col1, col2, col3 = st.columns(3)


        columns = [
            col1,
            col2,
            col3
        ]


        for position, (crop, score), column in zip(

            range(1, 4),

            top_3,

            columns

        ):

            with column:

                st.markdown(
                    f"""
<div class="rank-card">

<div class="rank-top">

<span class="rank-pos">
#{position}
</span>

<span class="rank-score">
{score:.1f}%
</span>

</div>

<div class="rank-name">
{crop.title()}
</div>

<div class="rank-track">

<div
class="rank-fill"
style="width:{min(score,100):.1f}%">
</div>

</div>

</div>
""",
                    unsafe_allow_html=True
                )


        spacer()


        # -------------------------------------------------
        # MODEL AGREEMENT
        # -------------------------------------------------

        section_header(
            "Model Agreement"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.info(
                f"Logistic Regression: "
                f"**{lr_prediction.title()}**"
            )


        with col2:

            st.success(
                f"Random Forest: "
                f"**{rf_prediction.title()}**"
            )


        if rf_prediction == lr_prediction:

            st.success(
                "✓ Both models agree on the recommended crop."
            )

        else:

            st.warning(
                "⚠ The two models produced different predictions."
            )


# =========================================================
# MODEL PERFORMANCE
# =========================================================

elif page == "📊 Model Performance":

    page_header(

        "Model Performance",

        "Comparison of the machine learning models trained for CropCompass."

    )


    section_header(
        "Model Comparison",
        "Test-set performance of the two trained classifiers."
    )


    comparison_df = pd.DataFrame({

        "Model": [
            "Logistic Regression",
            "Random Forest"
        ],

        "Accuracy": [
            97.27,
            99.55
        ],

        "Precision": [
            97.40,
            99.57
        ],

        "Recall": [
            97.27,
            99.55
        ],

        "F1 Score": [
            97.25,
            99.55
        ]

    })


    display_comparison = comparison_df.copy()


    for column in [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ]:

        display_comparison[column] = (
            display_comparison[column]
            .map(lambda x: f"{x:.2f}%")
        )


    st.dataframe(
        display_comparison,
        use_container_width=True,
        hide_index=True
    )


    spacer()


    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            """
<div class="model-card">

<div class="model-name">
Logistic Regression
</div>

<div class="model-accuracy">
97.27%
</div>

<div class="model-caption">
Test Accuracy
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
<div class="model-card model-card-selected">

<div class="model-name">
Random Forest
</div>

<div class="model-accuracy">
99.55%
</div>

<div class="model-caption">
Test Accuracy
</div>

<div class="model-badge">
✓ Selected model
</div>

</div>
""",
            unsafe_allow_html=True
        )


    spacer()


    # -----------------------------------------------------
    # FEATURE IMPORTANCE
    # -----------------------------------------------------

    section_header(

        "Random Forest Feature Importance",

        "Relative contribution of the seven input features to the trained model."

    )


    feature_importance = pd.DataFrame({

        "Feature": [

            "Rainfall",
            "Humidity",
            "K",
            "P",
            "N",
            "Temperature",
            "pH"

        ],

        "Importance": [

            21.96,
            21.71,
            18.08,
            15.13,
            10.34,
            7.55,
            5.23

        ]

    })


    feature_importance = (
        feature_importance
        .sort_values(
            "Importance",
            ascending=True
        )
    )


    st.bar_chart(

        feature_importance.set_index(
            "Feature"
        ),

        horizontal=True

    )


    st.caption(
        "Feature importance values are taken from the trained "
        "Random Forest model."
    )


# =========================================================
# EXPLAINABILITY
# =========================================================

elif page == "🔍 Explainability":

    page_header(

        "Prediction Explainability",

        "Understand which input features contributed to the "
        "Random Forest prediction."

    )


    section_header(

        "Input Conditions",

        "Enter the soil and environmental conditions for explanation."

    )


    col1, col2, col3 = st.columns(3)


    with col1:

        with st.container(border=True):

            st.markdown(
                '<div class="input-group-title">Soil Nutrients</div>',
                unsafe_allow_html=True
            )


            nitrogen = st.number_input(
                "Nitrogen (N)",
                min_value=0.0,
                max_value=140.0,
                value=50.0,
                step=0.1,
                key="shap_n"
            )


            phosphorus = st.number_input(
                "Phosphorus (P)",
                min_value=5.0,
                max_value=145.0,
                value=50.0,
                step=0.1,
                key="shap_p"
            )


            potassium = st.number_input(
                "Potassium (K)",
                min_value=5.0,
                max_value=205.0,
                value=50.0,
                step=0.1,
                key="shap_k"
            )


    with col2:

        with st.container(border=True):

            st.markdown(
                '<div class="input-group-title">Climate Conditions</div>',
                unsafe_allow_html=True
            )


            temperature = st.number_input(
                "Temperature (°C)",
                min_value=8.0,
                max_value=44.0,
                value=25.0,
                step=0.1,
                key="shap_temperature"
            )


            humidity = st.number_input(
                "Humidity (%)",
                min_value=14.0,
                max_value=100.0,
                value=70.0,
                step=0.1,
                key="shap_humidity"
            )


            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=20.0,
                max_value=299.0,
                value=100.0,
                step=0.1,
                key="shap_rainfall"
            )


    with col3:

        with st.container(border=True):

            st.markdown(
                '<div class="input-group-title">Soil Condition</div>',
                unsafe_allow_html=True
            )


            ph = st.number_input(
                "Soil pH",
                min_value=3.5,
                max_value=9.9,
                value=6.5,
                step=0.1,
                key="shap_ph"
            )


            st.markdown(
                """
<div class="info-note">

<b>SHAP explanation</b><br>

The analysis shows how each input feature
contributes to the selected model prediction.

</div>
""",
                unsafe_allow_html=True
            )


    spacer()


    explain_clicked = st.button(
        "🔍 Explain Prediction",
        use_container_width=True
    )


    if explain_clicked:

        input_data = pd.DataFrame(
            [{
                "N": nitrogen,
                "P": phosphorus,
                "K": potassium,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            }]
        )


        prediction = random_forest_model.predict(
            input_data
        )[0]


        probabilities = random_forest_model.predict_proba(
            input_data
        )[0]


        class_names = random_forest_model.classes_


        predicted_class_index = list(
            class_names
        ).index(
            prediction
        )


        prediction_score = (

            probabilities[
                predicted_class_index
            ]

            * 100

        )


        import shap


        explainer = shap.TreeExplainer(
            random_forest_model
        )


        shap_values = explainer.shap_values(
            input_data
        )


        if isinstance(
            shap_values,
            list
        ):

            feature_contributions = (
                shap_values[
                    predicted_class_index
                ][0]
            )

        elif len(
            shap_values.shape
        ) == 3:

            feature_contributions = (
                shap_values[
                    0,
                    :,
                    predicted_class_index
                ]
            )

        else:

            feature_contributions = (
                shap_values[0]
            )


        feature_names = list(
            input_data.columns
        )


        explanation_df = pd.DataFrame({

            "Feature":
                feature_names,

            "Input Value":
                input_data.iloc[0].values,

            "SHAP Value":
                feature_contributions

        })


        explanation_df["Impact"] = (

            explanation_df[
                "SHAP Value"
            ]

            .apply(

                lambda value:

                "Supports prediction"

                if value > 0

                else

                "Pushes away from prediction"

            )

        )


        explanation_df["Absolute Impact"] = (

            explanation_df[
                "SHAP Value"
            ].abs()

        )


        explanation_df = (

            explanation_df
            .sort_values(
                "Absolute Impact",
                ascending=False
            )

        )


        st.divider()


        section_header(

            "Prediction Explained",

            "Random Forest prediction and feature-level contribution."

        )


        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                f"""
<div class="result-box">

<div class="result-label">
Predicted Crop
</div>

<div class="result-crop">
{prediction.title()}
</div>

</div>
""",
                unsafe_allow_html=True
            )


        with col2:

            st.metric(
                "Model Score",
                f"{prediction_score:.2f}%"
            )


        spacer()


        section_header(

            "Feature Contribution",

            "Positive values support the predicted crop, while "
            "negative values push the prediction away from it."

        )


        chart_df = (

            explanation_df[
                ["Feature", "SHAP Value"]
            ]

            .set_index(
                "Feature"
            )

        )


        st.bar_chart(

            chart_df,

            horizontal=True

        )


        spacer()


        section_header(
            "Detailed Contributions"
        )


        display_df = explanation_df[
            [
                "Feature",
                "Input Value",
                "SHAP Value",
                "Impact"
            ]
        ].copy()


        display_df["SHAP Value"] = (

            display_df[
                "SHAP Value"
            ]

            .round(4)

        )


        st.dataframe(

            display_df,

            use_container_width=True,

            hide_index=True

        )


        strongest_feature = (
            explanation_df.iloc[0]
        )


        spacer()


        st.info(

            f"The feature with the strongest "
            f"contribution for this prediction is "
            f"**{strongest_feature['Feature']}**."

        )


        st.caption(

            "SHAP values explain the model's prediction "
            "for this input. They do not represent a direct "
            "causal effect on crop growth or agricultural outcomes."

        )


# =========================================================
# WHAT-IF ANALYSIS
# =========================================================

elif page == "🧪 What-If Analysis":

    page_header(

        "What-If Analysis",

        "Explore how changing one environmental condition "
        "can affect the model prediction."

    )


    section_header(

        "Baseline Conditions",

        "Start with a set of field conditions and then change one value."

    )


    col1, col2, col3 = st.columns(3)


    with col1:

        nitrogen = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            max_value=140.0,
            value=50.0,
            step=0.1,
            key="whatif_n"
        )


        phosphorus = st.number_input(
            "Phosphorus (P)",
            min_value=5.0,
            max_value=145.0,
            value=50.0,
            step=0.1,
            key="whatif_p"
        )


        potassium = st.number_input(
            "Potassium (K)",
            min_value=5.0,
            max_value=205.0,
            value=50.0,
            step=0.1,
            key="whatif_k"
        )


    with col2:

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=8.0,
            max_value=44.0,
            value=25.0,
            step=0.1,
            key="whatif_temperature"
        )


        humidity = st.number_input(
            "Humidity (%)",
            min_value=14.0,
            max_value=100.0,
            value=70.0,
            step=0.1,
            key="whatif_humidity"
        )


    with col3:

        ph = st.number_input(
            "Soil pH",
            min_value=3.5,
            max_value=9.9,
            value=6.5,
            step=0.1,
            key="whatif_ph"
        )


        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=20.0,
            max_value=299.0,
            value=100.0,
            step=0.1,
            key="whatif_rainfall"
        )


    spacer()


    section_header(

        "Change One Condition",

        "The model is not retrained. Only the input value is changed."

    )


    feature_options = {

        "Nitrogen (N)": (
            "N",
            0.0,
            140.0,
            nitrogen
        ),

        "Phosphorus (P)": (
            "P",
            5.0,
            145.0,
            phosphorus
        ),

        "Potassium (K)": (
            "K",
            5.0,
            205.0,
            potassium
        ),

        "Temperature (°C)": (
            "temperature",
            8.0,
            44.0,
            temperature
        ),

        "Humidity (%)": (
            "humidity",
            14.0,
            100.0,
            humidity
        ),

        "Soil pH": (
            "ph",
            3.5,
            9.9,
            ph
        ),

        "Rainfall (mm)": (
            "rainfall",
            20.0,
            299.0,
            rainfall
        )

    }


    selected_feature = st.selectbox(

        "Select feature to change",

        list(
            feature_options.keys()
        )

    )


    feature_key, min_value, max_value, current_value = (
        feature_options[
            selected_feature
        ]
    )


    changed_value = st.number_input(

        f"New value for {selected_feature}",

        min_value=min_value,

        max_value=max_value,

        value=float(current_value),

        step=0.1,

        key="whatif_changed_value"

    )


    spacer()


    if st.button(

        "🧪 Run What-If Analysis",

        use_container_width=True

    ):


        baseline_data = pd.DataFrame(
            [{
                "N": nitrogen,
                "P": phosphorus,
                "K": potassium,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            }]
        )


        changed_data = baseline_data.copy()


        changed_data.loc[
            0,
            feature_key
        ] = changed_value


        # -------------------------------------------------
        # BASELINE
        # -------------------------------------------------

        baseline_prediction = (
            random_forest_model
            .predict(
                baseline_data
            )[0]
        )


        baseline_probabilities = (
            random_forest_model
            .predict_proba(
                baseline_data
            )[0]
        )


        baseline_classes = (
            random_forest_model
            .classes_
        )


        baseline_top_indices = (
            baseline_probabilities
            .argsort()[::-1][:3]
        )


        baseline_top3 = [

            (
                baseline_classes[i],
                baseline_probabilities[i] * 100
            )

            for i in baseline_top_indices

        ]


        # -------------------------------------------------
        # CHANGED
        # -------------------------------------------------

        changed_prediction = (
            random_forest_model
            .predict(
                changed_data
            )[0]
        )


        changed_probabilities = (
            random_forest_model
            .predict_proba(
                changed_data
            )[0]
        )


        changed_classes = (
            random_forest_model
            .classes_
        )


        changed_top_indices = (
            changed_probabilities
            .argsort()[::-1][:3]
        )


        changed_top3 = [

            (
                changed_classes[i],
                changed_probabilities[i] * 100
            )

            for i in changed_top_indices

        ]


        st.divider()


        section_header(
            "What Changed?"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                f"""
<div class="model-card">

<div class="model-name">
Baseline
</div>

<div class="model-accuracy"
style="font-size:32px;">
{baseline_prediction.title()}
</div>

<div class="model-caption">
Original value: {current_value:.1f}
</div>

</div>
""",
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                f"""
<div class="model-card model-card-selected">

<div class="model-name">
After Change
</div>

<div class="model-accuracy"
style="font-size:32px;">
{changed_prediction.title()}
</div>

<div class="model-caption">
New value: {changed_value:.1f}
</div>

</div>
""",
                unsafe_allow_html=True
            )


        spacer()


        if baseline_prediction == changed_prediction:

            st.success(

                f"The predicted crop remained "
                f"**{changed_prediction.title()}** after changing "
                f"{selected_feature}."

            )

        else:

            st.warning(

                f"The prediction changed from "
                f"**{baseline_prediction.title()}** to "
                f"**{changed_prediction.title()}** "
                f"after changing {selected_feature}."

            )


        spacer()


        section_header(
            "Top 3 Before vs After"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                "### Baseline"
            )


            for position, (crop, score) in enumerate(
                baseline_top3,
                start=1
            ):

                st.write(
                    f"**#{position} {crop.title()}** — "
                    f"{score:.1f}%"
                )


        with col2:

            st.markdown(
                "### Changed"
            )


            for position, (crop, score) in enumerate(
                changed_top3,
                start=1
            ):

                st.write(
                    f"**#{position} {crop.title()}** — "
                    f"{score:.1f}%"
                )


        st.caption(

            "What-If Analysis shows how the trained model "
            "responds to a changed input. It does not mean "
            "that changing one real-world condition alone "
            "will guarantee a different crop outcome."

        )


# =========================================================
# PREDICTION HISTORY
# =========================================================

elif page == "📜 Prediction History":

    page_header(

        "Prediction History",

        "View previous crop predictions generated through CropCompass."

    )


    history_df = load_prediction_history()


    if history_df.empty:

        st.info(

            "No predictions have been recorded yet. "
            "Run a prediction from the Crop Prediction page "
            "to create your first history entry."

        )

    else:

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Total Predictions",
                len(history_df)
            )


        with col2:

            st.metric(

                "Latest Recommendation",

                history_df.iloc[0][
                    "Random Forest"
                ].title()

            )


        with col3:

            average_score = history_df[
                "RF Score"
            ].mean()

            st.metric(

                "Average RF Score",

                f"{average_score:.1f}%"

            )


        spacer()


        section_header(

            "Recent Predictions",

            "Most recent predictions are shown first."

        )


        display_history = history_df.copy()


        display_history["RF Score"] = (
            display_history["RF Score"]
            .map(
                lambda x:
                f"{x:.2f}%"
            )
        )


        st.dataframe(

            display_history,

            use_container_width=True,

            hide_index=True

        )


        spacer()


        section_header(
            "Prediction Summary"
        )


        crop_counts = (
            history_df[
                "Random Forest"
            ]
            .value_counts()
            .reset_index()
        )


        crop_counts.columns = [
            "Crop",
            "Predictions"
        ]


        st.bar_chart(

            crop_counts.set_index(
                "Crop"
            )

        )


        st.caption(

            "Prediction history is stored locally in "
            "database/cropcompass.db."

        )


# =========================================================
# DATASET & EDA
# =========================================================

elif page == "📈 Dataset & EDA":

    page_header(

        "Dataset & Exploratory Data Analysis",

        "Explore the Crop Recommendation Dataset used to train "
        "the CropCompass models."

    )


    if dataset is None:

        st.error(

            "Crop_recommendation.csv was not found. "
            "Place the dataset in the project folder or "
            "inside a data/ or dataset/ folder."

        )

    else:

        # -------------------------------------------------
        # DATASET OVERVIEW
        # -------------------------------------------------

        section_header(

            "Dataset Overview",

            "Basic information about the dataset used by CropCompass."

        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Records",
                f"{len(dataset):,}"
            )


        with col2:

            st.metric(
                "Columns",
                len(dataset.columns)
            )


        with col3:

            st.metric(
                "Crop Classes",
                dataset["label"].nunique()
            )


        with col4:

            st.metric(

                "Missing Values",

                int(
                    dataset.isnull()
                    .sum()
                    .sum()
                )

            )


        spacer()


        # -------------------------------------------------
        # DATASET PREVIEW
        # -------------------------------------------------

        section_header(

            "Dataset Preview",

            "First rows of the Crop Recommendation Dataset."

        )


        st.dataframe(

            dataset.head(10),

            use_container_width=True,

            hide_index=True

        )


        spacer()


        # -------------------------------------------------
        # DATA QUALITY
        # -------------------------------------------------

        section_header(
            "Data Quality"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(

                "Missing Values",

                int(
                    dataset.isnull()
                    .sum()
                    .sum()
                )

            )


        with col2:

            st.metric(

                "Duplicate Rows",

                int(
                    dataset.duplicated()
                    .sum()
                )

            )


        with col3:

            st.metric(

                "Features",

                len(
                    dataset.columns
                ) - 1

            )


        spacer()


        # -------------------------------------------------
        # CROP DISTRIBUTION
        # -------------------------------------------------

        section_header(

            "Crop Class Distribution",

            "The dataset contains 22 crop classes."

        )


        class_distribution = (

            dataset["label"]
            .value_counts()
            .sort_values(
                ascending=False
            )

        )


        st.bar_chart(
            class_distribution
        )


        spacer()


        # -------------------------------------------------
        # NUMERICAL STATISTICS
        # -------------------------------------------------

        section_header(

            "Numerical Feature Statistics",

            "Summary statistics for the seven input features."

        )


        st.dataframe(

            dataset.describe()
            .round(3),

            use_container_width=True

        )


        spacer()


        # -------------------------------------------------
        # FEATURE DISTRIBUTION
        # -------------------------------------------------

        section_header(

            "Feature Distribution",

            "Explore the distribution of individual numerical features."

        )


        numeric_features = [

            "N",
            "P",
            "K",
            "temperature",
            "humidity",
            "ph",
            "rainfall"

        ]


        selected_feature = st.selectbox(

            "Select feature",

            numeric_features

        )


        st.bar_chart(

            dataset[selected_feature]
            .value_counts()
            .sort_index()

        )


        spacer()


        # -------------------------------------------------
        # CORRELATION
        # -------------------------------------------------

        section_header(

            "Feature Correlation",

            "Correlation values between numerical input features."

        )


        correlation_df = (

            dataset[
                numeric_features
            ]

            .corr()

            .round(2)

        )


        st.dataframe(

            correlation_df,

            use_container_width=True

        )


        st.caption(

            "Correlation describes statistical association "
            "between numerical variables; it does not imply causation."

        )


# =========================================================
# END
# =========================================================