import { useMutation } from '@tanstack/react-query';
import { queryService } from '../services/queryService';
import { QueryResponseData } from '../types';
import { toast } from 'sonner';

interface QueryVariables {
  question: string;
  videoId?: number | null;
}

export const useQueryRAG = () => {
  return useMutation<QueryResponseData, Error, QueryVariables>({
    mutationFn: ({ question, videoId }) =>
      queryService.askQuestion(question, videoId),

    onError: (error: Error) => {
      toast.error(`AI query failed: ${error.message}`);
    },
  });
};
