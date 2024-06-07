import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useParams } from "react-router-dom"
import { getGame, join } from "../network/requests"
import Board from "../components/Board"

export default function GamePage() {

    const { id } = useParams()

    const { data, isSuccess } = useQuery({
        queryKey: ["games", id],
        queryFn: () => getGame(id!),
        enabled: !!id
    })


    if (!isSuccess) return <div>Loading...</div>

    return <div className="flex items-center justify-center">
        <Board gameInfo={data} />
    </div>
}