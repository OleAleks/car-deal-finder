import streamlit as st


def create_filter_sidebar(df):
    """
        Create Streamlit sidebar for hierarchical filtering
    """
    st.sidebar.header("Car Deal Filters")

    #selecting brand
    brands = ["All"] + list(df["brand"].unique())
    selected_brand = st.sidebar.selectbox("Select Brand", brands)

    #model Selection only after brand selection
    if selected_brand == "All":
        st.sidebar.warning("Please select a brand to filter models")
        selected_model = None
        filtered_df = df
    else:
        # Filter models based on selected brand
        filtered_df = df[df["brand"] == selected_brand]
        models = ["All"] + list(filtered_df["model"].unique())
        selected_model = st.sidebar.selectbox("Select Model", models)

    #only when brand and model selected more filters available
    if selected_brand != "All" and selected_model != "All":
        #more filter by model
        filtered_df = filtered_df[filtered_df["model"] == selected_model]

        #check for only one data or else streamlit error
        km_min = int(filtered_df["kmdriven"].min())
        km_max = int(filtered_df["kmdriven"].max())

        if km_min == km_max:
            st.sidebar.write(f"Kilometers Driven: {km_min} (only one value available)")
            km_range = (km_min, km_max)
        else:
        #adjust kilometers driven slider based on current data filter
            km_range = st.sidebar.slider(
                "Kilometers Driven",
                min_value=km_min,
                max_value=km_max,
                value=(km_min, km_max)
            )

        #relative Price Classification filter
        price_classifications = ["All", "Very Cheap", "Cheap", "Average", "Expensive", "Very Expensive"]
        selected_price_classification = st.sidebar.selectbox(
            "Select Price Classification",
            price_classifications
        )
    else:
        km_range = (None, None)
        selected_price_classification = "All"
        filtered_df = df

    #create dictionary of filters
    filters = {
        "brand": selected_brand if selected_brand != "All" else None,
        "model": selected_model if selected_model and selected_model != "All" else None,
        "kmdriven": km_range,
        "price_classification": selected_price_classification
    }

    return filters, filtered_df


def apply_filters(df, filters):
    """
        Apply filters to a copy of the DataFrame
        :param df: transformed DataFrame
        :param filters: dictionary of filters
        :return df: DataFrame with applied filters
    """
    filtered_df = df.copy()

    # Brand filter
    if filters["brand"]:
        filtered_df = filtered_df[filtered_df["brand"] == filters["brand"]]

    # Model filter
    if filters["model"]:
        filtered_df = filtered_df[filtered_df["model"] == filters["model"]]

    # Kilometers driven filter
    if filters["kmdriven"] != (None, None):
        filtered_df = filtered_df[
            filtered_df["kmdriven"].between(
                filters["kmdriven"][0],
                filters["kmdriven"][1]
            )
        ]

    # Price classification filter
    if filters["price_classification"] != "All":
        filtered_df = filtered_df[
            filtered_df["priceclassification"] == filters["price_classification"]
            ]

    return filtered_df, len(filtered_df)