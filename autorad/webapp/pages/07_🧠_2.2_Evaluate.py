import seaborn as sns
import streamlit as st

from autorad.evaluation.evaluator import SimpleEvaluator
from autorad.webapp import template_utils, utils


def show():
    template_utils.show_title()

    st.write(
        """
        Analyze the results with most widely used metrics such as
        AUC ROC curve, precision-recall curve and confusion matrix.
        """
    )
    result_df = utils.load_df("Choose a CSV file with predictions:")
    col1, col2 = st.columns(2)
    with col1:
        cm = sns.light_palette("blue", as_cmap=True)
        st.dataframe(result_df.style.background_gradient(cmap=cm))
    result_df_colnames = result_df.columns.tolist()
    with col2:
        label = st.selectbox("Select the label column", result_df_colnames)
    with col2:
        pred = st.selectbox("Select the prediction column", result_df_colnames)
    # Evaluation
    evaluate = st.button("Evaluate!")
    if evaluate:
        evaluator = SimpleEvaluator(
            y_true=result_df[label].tolist(),
            y_pred_proba=result_df[pred].tolist(),
        )
        col1, col2 = st.columns(2)
        with col1:
            st.write(evaluator.plot_roc_curve())
        with col2:
            st.write(evaluator.plot_precision_recall_curve())
        fig = evaluator.plot_waterfall()
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    show()
