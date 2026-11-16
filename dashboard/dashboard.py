"""
Dashboard interaktif - Air Quality Dataset Beijing (2013-2017)
Dicoding "Belajar Analisis Data dengan Python" - Final Project

Jalankan dengan:
    streamlit run dashboard.py
(pastikan file main_data.csv berada di folder yang sama)
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_style("whitegrid")

st.set_page_config(
    page_title="Air Quality Dashboard - Beijing",
    page_icon="🌫️",
    layout="wide",
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_DIR, "main_data.csv")

CATEGORY_ORDER = [
    "Good", "Moderate", "Unhealthy (Sensitive)",
    "Unhealthy", "Very Unhealthy", "Hazardous",
]
CATEGORY_COLORS = {
    "Good": "#4daf4a",
    "Moderate": "#ffe066",
    "Unhealthy (Sensitive)": "#ff9f40",
    "Unhealthy": "#f0544f",
    "Very Unhealthy": "#8f3f97",
    "Hazardous": "#7e0023",
}
SEASON_ORDER = ["Spring", "Summer", "Autumn", "Winter"]


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["datetime"])
    df["date"] = pd.to_datetime(df["date"])
    df["AQI_category"] = pd.Categorical(
        df["AQI_category"], categories=CATEGORY_ORDER, ordered=True
    )
    df["season"] = pd.Categorical(df["season"], categories=SEASON_ORDER, ordered=True)
    return df


if not os.path.exists(DATA_PATH):
    st.error(
        "File `main_data.csv` tidak ditemukan di folder `dashboard/`. "
        "Pastikan berkas tersebut ada sebelum menjalankan dashboard."
    )
    st.stop()

main_df = load_data(DATA_PATH)

# ---------------------------------------------------------------------------
# SIDEBAR - FILTER
# ---------------------------------------------------------------------------
st.sidebar.title("🌫️ Air Quality Dashboard")
st.sidebar.markdown("**Beijing Multi-Site Air Quality (2013–2017)**")
st.sidebar.markdown("---")

min_date = main_df["date"].min().date()
max_date = main_df["date"].max().date()

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

all_stations = sorted(main_df["station"].unique())
selected_stations = st.sidebar.multiselect(
    "Pilih Stasiun", options=all_stations, default=all_stations
)

pollutant = st.sidebar.selectbox(
    "Polutan Utama",
    options=["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Dataset: PRSA Beijing Multi-Site Air-Quality Data "
    "([sumber](https://github.com/marceloreis/HTI/tree/master))"
)

mask = (
    (main_df["date"].dt.date >= start_date)
    & (main_df["date"].dt.date <= end_date)
    & (main_df["station"].isin(selected_stations))
)
filtered_df = main_df.loc[mask].copy()

st.title("Dashboard Analisis Kualitas Udara Kota Beijing")
st.markdown(
    "Dashboard ini merangkum hasil analisis data kualitas udara dari **12 "
    "stasiun pemantauan** di Beijing periode **Maret 2013 – Februari 2017**. "
    "Gunakan filter pada sidebar untuk menjelajahi data berdasarkan rentang "
    "tanggal, stasiun, dan polutan."
)

if filtered_df.empty:
    st.warning("Tidak ada data pada filter yang dipilih. Silakan ubah filter.")
    st.stop()

# ---------------------------------------------------------------------------
# KPI METRICS
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
avg_val = filtered_df[pollutant].mean()
max_val = filtered_df[pollutant].max()
worst_row = (
    filtered_df.groupby("station")[pollutant].mean().idxmax()
)
pct_unhealthy = (
    filtered_df["AQI_category"].isin(
        ["Unhealthy", "Very Unhealthy", "Hazardous"]
    ).mean()
    * 100
)

col1.metric(f"Rata-rata {pollutant}", f"{avg_val:,.1f} µg/m³")
col2.metric(f"Nilai {pollutant} Tertinggi", f"{max_val:,.1f} µg/m³")
col3.metric("Stasiun Paling Tercemar (rata-rata)", worst_row)
col4.metric("% Jam Kategori Unhealthy+", f"{pct_unhealthy:.1f}%")

st.markdown("---")

# ---------------------------------------------------------------------------
# TABS
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Tren Waktu",
        "🏙️ Perbandingan Stasiun",
        "🗺️ Geospatial",
        "🧩 Kategori Kualitas Udara",
    ]
)

# --- TAB 1: Tren waktu ----------------------------------------------------
with tab1:
    st.subheader(f"Tren Rata-rata {pollutant} Bulanan")
    monthly = (
        filtered_df.set_index("datetime")
        .resample("ME")[pollutant]
        .mean()
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(monthly["datetime"], monthly[pollutant], color="#C44E52", linewidth=2)
    ax.set_xlabel("Bulan")
    ax.set_ylabel(f"Rata-rata {pollutant} (µg/m³)")
    ax.set_title(f"Tren Bulanan {pollutant} (Stasiun Terpilih)")
    st.pyplot(fig)
    plt.close(fig)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader(f"Rata-rata {pollutant} per Jam")
        hourly = filtered_df.groupby("hour")[pollutant].mean().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.lineplot(data=hourly, x="hour", y=pollutant, marker="o", ax=ax, color="#4C72B0")
        ax.set_xlabel("Jam")
        ax.set_ylabel(f"Rata-rata {pollutant} (µg/m³)")
        ax.set_xticks(range(0, 24, 4))
        st.pyplot(fig)
        plt.close(fig)
    with c2:
        st.subheader(f"Rata-rata {pollutant} per Musim")
        season_avg = (
            filtered_df.groupby("season", observed=True)[pollutant]
            .mean()
            .reindex(SEASON_ORDER)
            .reset_index()
        )
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(data=season_avg, x="season", y=pollutant, hue="season",
                    palette="rocket", legend=False, ax=ax)
        ax.set_xlabel("Musim")
        ax.set_ylabel(f"Rata-rata {pollutant} (µg/m³)")
        st.pyplot(fig)
        plt.close(fig)

# --- TAB 2: Perbandingan stasiun ------------------------------------------
with tab2:
    st.subheader(f"Perbandingan Rata-rata {pollutant} Antar Stasiun")
    station_avg = (
        filtered_df.groupby("station")[pollutant]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=station_avg, y="station", x=pollutant, hue="station",
                palette="YlOrRd_r", legend=False, ax=ax)
    ax.set_xlabel(f"Rata-rata {pollutant} (µg/m³)")
    ax.set_ylabel("Stasiun")
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("Lihat tabel data"):
        st.dataframe(station_avg, width="stretch")

# --- TAB 3: Geospatial ------------------------------------------------------
with tab3:
    st.subheader(f"Sebaran Spasial Rata-rata {pollutant} Antar Stasiun")
    geo_avg = (
        filtered_df.groupby(["station", "lat", "lon"])[pollutant]
        .mean()
        .reset_index()
    )

    c1, c2 = st.columns([1.3, 1])
    with c1:
        fig, ax = plt.subplots(figsize=(7, 6.5))
        sc = ax.scatter(
            geo_avg["lon"], geo_avg["lat"],
            s=geo_avg[pollutant] * 6, c=geo_avg[pollutant],
            cmap="YlOrRd", edgecolor="black", linewidth=0.6, alpha=0.9,
        )
        for _, row in geo_avg.iterrows():
            ax.annotate(row["station"], (row["lon"], row["lat"]),
                        textcoords="offset points", xytext=(5, 4), fontsize=8)
        cbar = plt.colorbar(sc, ax=ax)
        cbar.set_label(f"Rata-rata {pollutant} (µg/m³)")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        st.pyplot(fig)
        plt.close(fig)
    with c2:
        st.markdown("**Peta lokasi stasiun** (basemap, butuh koneksi internet):")
        try:
            st.map(geo_avg.rename(columns={"lat": "latitude", "lon": "longitude"}),
                   latitude="latitude", longitude="longitude", size=pollutant)
        except Exception:
            st.info("Basemap tidak dapat dimuat (tidak ada koneksi internet).")
        st.dataframe(
            geo_avg.sort_values(pollutant, ascending=False).reset_index(drop=True),
            width="stretch",
        )

# --- TAB 4: Kategori kualitas udara ----------------------------------------
with tab4:
    st.subheader("Distribusi Kategori Kualitas Udara (Binning PM2.5)")
    st.caption(
        "Kategori dibentuk melalui binning manual (tanpa machine learning) "
        "berdasarkan breakpoint standar PM2.5 24-jam."
    )

    c1, c2 = st.columns(2)
    with c1:
        cat_counts = (
            filtered_df["AQI_category"].value_counts(normalize=True)
            .reindex(CATEGORY_ORDER).fillna(0) * 100
        )
        fig, ax = plt.subplots(figsize=(6, 4.5))
        ax.bar(cat_counts.index, cat_counts.values,
               color=[CATEGORY_COLORS[c] for c in cat_counts.index])
        ax.set_ylabel("Persentase Observasi (%)")
        ax.set_xticks(range(len(cat_counts.index)))
        ax.set_xticklabels(cat_counts.index, rotation=30, ha="right")
        ax.set_title("Proporsi Kategori Kualitas Udara")
        st.pyplot(fig)
        plt.close(fig)

    with c2:
        counts = (
            filtered_df.groupby(["season", "AQI_category"], observed=True)
            .size().unstack(fill_value=0)
        )
        cat_season = counts.div(counts.sum(axis=1), axis=0) * 100
        cat_season = cat_season.reindex(SEASON_ORDER)[CATEGORY_ORDER].fillna(0)

        fig, ax = plt.subplots(figsize=(6, 4.5))
        cat_season.plot(
            kind="bar", stacked=True, ax=ax,
            color=[CATEGORY_COLORS[c] for c in CATEGORY_ORDER], width=0.65,
        )
        ax.set_ylabel("Persentase Observasi (%)")
        ax.set_xlabel("Musim")
        ax.set_title("Kategori Kualitas Udara per Musim")
        ax.legend(title="Kategori", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
        plt.xticks(rotation=0)
        st.pyplot(fig)
        plt.close(fig)

st.markdown("---")
st.caption(
    "Dibuat untuk proyek akhir kelas Dicoding 'Belajar Analisis Data dengan "
    "Python'. Sumber data: Beijing Multi-Site Air-Quality Data (PRSA), "
    "2013–2017."
)
