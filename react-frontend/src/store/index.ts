// src/store/index.ts

import { configureStore } from '@reduxjs/toolkit';
import articlesReducer from './articlesSlice';

const store = configureStore({
  reducer: {
    articles: articlesReducer,
  },
});

export default store;
