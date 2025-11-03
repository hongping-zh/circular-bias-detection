export interface ReviewSection {
  title: string;
  content: string;
}

export interface JossReview {
  summary: string;
  sections: ReviewSection[];
}
