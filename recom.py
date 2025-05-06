# Core Pkg
import streamlit as st 
import streamlit.components.v1 as stc 

# Load EDA
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Our Dataset
def load_data(data):
    df = pd.read_csv(data)
    return df 

# Vectorize + Cosine Similarity Matrix
def vectorize_text_to_cosine_mat(data):
    count_vect = CountVectorizer()
    cv_mat = count_vect.fit_transform(data)
    # Get the cosine
    cosine_sim_mat = cosine_similarity(cv_mat)
    return cosine_sim_mat

# Recommendation Sys
@st.cache_data
def get_recommendation(title, cosine_sim_mat, df, num_of_rec=10):
    # indices of the course
    course_indices = pd.Series(df.index, index=df['course_title']).drop_duplicates()
    
    # Index of course
    idx = course_indices[title]

    # Look into the cosine matr for that index
    sim_scores = list(enumerate(cosine_sim_mat[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    selected_course_indices = [i[0] for i in sim_scores[1:]]
    selected_course_scores = [i[1] for i in sim_scores[1:]]  # Fixed: Use i[1] for scores

    # Get the dataframe & title
    result_df = df.iloc[selected_course_indices]
    result_df['similarity_score'] = selected_course_scores
    final_recommended_courses = result_df[['course_title', 'similarity_score', 'url', 'price', 'num_subscribers']]
    return final_recommended_courses.head(num_of_rec)

RESULT_TEMP = """
<div style="width:90%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 60px;
box-shadow:0 0 15px 5px #ccc; background-color: #a8f0c6;
  border-left: 5px solid #6c6c6c;">
<h4>{}</h4>
<p style="color:blue;"><span style="color:black;">📈Score::</span>{}</p>
<p style="color:blue;"><span style="color:black;">🔗</span><a href="{}" target="_blank">Link</a></p>
<p style="color:blue;"><span style="color:black;">💲Price:</span>{}</p>
<p style="color:blue;"><span style="color:black;">🧑‍🎓👨🏽‍🎓 Students:</span>{}</p>

</div>
"""

# Search For Course 
@st.cache_data
def search_term_if_not_found(term, df):
    result_df = df[df['course_title'].str.contains(term, case=False)]  # Added case=False for better matching
    return result_df

def main():
    st.title("Course Recommendation App")

    menu = ["Home", "Recommend"]
    choice = st.sidebar.selectbox("Menu", menu)

    try:
        df = load_data("recom.csv")
        
        if choice == "Home":
            st.subheader("Home")
            st.dataframe(df.head(10))

        elif choice == "Recommend":
            st.subheader("Recommend Courses")
            
            # Only compute cosine similarity if we have data
            if not df.empty:
                cosine_sim_mat = vectorize_text_to_cosine_mat(df['course_title'])
                
                search_term = st.text_input("Search")
                num_of_rec = st.sidebar.number_input("Number of Recommendations", 4, 30, 7)
                
                if st.button("Recommend"):
                    if search_term:
                        try:
                            # Check if search term exists in the course titles
                            if search_term in df['course_title'].values:
                                results = get_recommendation(search_term, cosine_sim_mat, df, num_of_rec)
                                
                                # Display as JSON
                                with st.expander("Results as JSON"):  # Changed from beta_expander to expander
                                    results_json = results.to_dict('index')
                                    st.write(results_json)

                                # Display as cards
                                for row in results.iterrows():
                                    rec_title = row[1]['course_title']
                                    rec_score = row[1]['similarity_score']
                                    rec_url = row[1]['url']
                                    rec_price = row[1]['price']
                                    rec_num_sub = row[1]['num_subscribers']

                                    stc.html(RESULT_TEMP.format(rec_title, rec_score, rec_url, rec_price, rec_num_sub), height=350)
                            else:
                                st.info("Course not found. Suggested options include:")
                                result_df = search_term_if_not_found(search_term, df)
                                if not result_df.empty:
                                    st.dataframe(result_df)
                                else:
                                    st.warning("No matching courses found. Try a different search term.")
                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                            st.info("Suggested options based on your search:")
                            result_df = search_term_if_not_found(search_term, df)
                            if not result_df.empty:
                                st.dataframe(result_df)
                            else:
                                st.warning("No matching courses found. Try a different search term.")
            else:
                st.error("Dataset is empty. Please check your CSV file.")
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.info("Please make sure 'recom.csv' is in the same directory as your script.")

if __name__ == '__main__':
    main()